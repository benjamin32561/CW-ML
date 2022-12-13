using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using Microsoft.ML.OnnxRuntime;
using Microsoft.ML.OnnxRuntime.Tensors;

namespace Server_Usage
{
    class AccidentClassifier
    {
        private InferenceSession session; //the onnx session
        private float threshold; //the classification threshold
        private int input_rows;
        private int input_cols;

        /*
        C'tor creates the class and intializes private variables.
        input:
            -string model_path: path to the model .onnx file
            -float threshold: the classification threshold, above the threshold is accident
        */
        public AccidentClassifier(string model_path, float threshold = 0.5f)
        {
            this.session = new InferenceSession(model_path);
            this.threshold = threshold;
            int[] input_dimensons = this.session.InputMetadata["modelInput"].Dimensions;
            this.input_rows = input_dimensons[1];
            this.input_cols = input_dimensons[2];
        }

        /*
        this function gets a recording as float array and converts it to DenseTensor 
        input:
            -float[,] recording: the recording as float array, [677,3]
        output:
            -DenseTensor<float>: the recording as a tensor
        */
        private DenseTensor<float> ArrayToDenseTensor(float[,] recording)
        {
            DenseTensor<float> to_ret = new DenseTensor<float>(new[] { 1, this.input_rows, this.input_cols});
            for(int i = 0; i<recording.GetLength(0);i++)
            {
                for (int j = 0; j < recording.GetLength(1); j++)
                {
                    to_ret[0,i,j] = recording[i,j];
                }
            }
            return to_ret;
        }

        /*
        This function adds zero row buffers to an array to match number of rows model expects
        input:
            -float[,] arr: original array to add rows to
            -int add_start: number of rows to add at the beggining of the array
            -int add_end: number of rows to add at the end of the array
        */
        public float[,] AddBufferRows(float[,] arr, int add_start, int add_end)
        {
            int n_cols = arr.GetLength(1);
            int n_original_row = arr.GetLength(0);
            int n_final_rows = add_start + add_end + n_original_row;
            float[,] to_ret = new float[n_final_rows, n_cols];
            to_ret[n_final_rows - 1, n_cols - 1]=0;
            for (int i = 0; i < n_final_rows; i++)
            {
                for (int j = 0; j < n_cols; j++)
                {
                    if (i < n_original_row && i >= add_start)
                        to_ret[i, j] = arr[i, j];
                    else
                        to_ret[i, j] = 0;
                }
            }
            return to_ret;
        }

        /*
        This function removes spare rows from an array to match number of rows model expects
        input:
            -float[,] arr: original array to remove rows from
            -int remove_start: number of rows to remove from the beggining of the array
            -int remove_end: number of rows to remove from the end of the array
        */
        public float[,] RemoveRows(float[,] arr, int remove_start, int remove_end)
        {
            int n_cols = arr.GetLength(1);
            int n_original_row = arr.GetLength(0);
            int n_final_rows = n_original_row - remove_start - remove_end;
            float[,] to_ret = new float[n_final_rows, n_cols];
            for (int i = remove_start; i < n_original_row-remove_end; i++)
            {
                for (int j = 0; j < n_cols; j++)
                    to_ret[i- remove_start, j] = arr[i, j];
            }
            return to_ret;
        }

        /*
        This function fix number of rows in an array to match model expectation,
        removing rows from the start and end or adding buffers to the start and end
        input:
            -float[,] arr: original array to fix
        */
        private float[,] FixRows(float[,] arr)
        {
            int org_diff = this.input_rows - arr.GetLength(0);
            int diff = Math.Abs(org_diff);
            int change = diff / 2;
            int start = change;
            int end = change;
            if (diff % 2 != 0)
                start += 1;
            if (org_diff > 0)
            {
                return AddBufferRows(arr, start, end);
            }
            return RemoveRows(arr, start, end);
        }

        /*
        This function adds zero col buffers to an array to match number of cols model expects
        input:
            -float[,] arr: original array to add cols to
            -int add_start: number of cols to add at the beggining of the array
            -int add_end: number of cols to add at the end of the array
        */
        public float[,] AddBufferCols(float[,] arr, int add_start, int add_end)
        {
            int n_cols = arr.GetLength(1);
            int n_rows = arr.GetLength(0);
            int n_final_cols = n_cols + add_start + add_end;
            float[,] to_ret = new float[n_rows, n_final_cols];
            for (int i = 0; i < n_rows; i++)
            {
                for (int j = 0; j < n_final_cols; j++)
                {
                    if (j < n_cols && i >= add_start)
                        to_ret[i, j] = arr[i, j];
                    else
                        to_ret[i, j] = 0;
                }
            }
            return to_ret;
        }

        /*
        This function removes spare cols from an array to match number of cols model expects
        input:
            -float[,] arr: original array to remove cols from
            -int remove_start: number of cols to remove from the beggining of the array
            -int remove_end: number of cols to remove from the end of the array
        */
        public float[,] RemoveCols(float[,] arr, int remove_start, int remove_end)
        {
            int n_cols = arr.GetLength(1);
            int n_rows = arr.GetLength(0);
            int n_final_cols = n_cols - remove_start - remove_end;
            float[,] to_ret = new float[n_rows, n_final_cols];
            for (int i = 0; i < n_rows; i++)
            {
                for (int j = remove_start; j < remove_end; j++)
                    to_ret[i, j] = arr[i, j];
            }
            return to_ret;
        }

        /*
        This function fix number of cols in an array to match model expectation,
        removing cols from the start and end or adding buffers to the start and end
        input:
            -float[,] arr: original array to fix
        */
        private float[,] FixCols(float[,] arr)
        {
            int org_diff = this.input_cols - arr.GetLength(1);
            int diff = Math.Abs(org_diff);
            int change = diff / 2;
            int start = change;
            int end = change;
            if (diff % 2 != 0)
                start += 1;
            if (org_diff > 0)
            {
                return AddBufferCols(arr, start, end);
            }
            return RemoveCols(arr, start, end);
        }

        /*
        this function gets a recording as float array and gives the model prediction value
        input:
            -float[,] recording: the recording as float array, [677,3]
        output:
            -float: the model prediction, model output
        */
        public float MakePrediction(float[,] recording)
        {
            if (recording.GetLength(0) != this.input_rows)
                recording = this.FixRows(recording);
            if (recording.GetLength(1) != this.input_cols)
                recording= this.FixCols(recording);
            DenseTensor<float> arr_as_tens = this.ArrayToDenseTensor(recording);
            var inputs = new List<NamedOnnxValue> { NamedOnnxValue.CreateFromTensor("modelInput", arr_as_tens) };
            var output = this.session.Run(inputs).First().AsTensor<float>();
            return output[0];
        }

        /*
        this function gets a recording as float array and returns whether the model
        predicted if it comtains an accidint
        input:
            -float[,] recording: the recording as string, [677,3]
        output:
            -bool: does the recording contain an accident
        */
        public bool AccidentOrNot(float[,] recording)
        {
            float prediction = this.MakePrediction(recording);
            return prediction >= this.threshold;
        }

        /*
        this function gets a float, the model output, and based on the threshold decides if there was an accident
        input:
            -float prediction: the model output for a recording
        output:
            -bool: did the model predict an accident
        */
        public bool AccidentOrNot(float prediction)
        {
            return prediction >= this.threshold;
        }
    }
}
