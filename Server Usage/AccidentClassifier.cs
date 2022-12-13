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
        private InferenceSession session;
        private float threshold;

        public AccidentClassifier(string model_path, float threshold = 0.5f)
        {
            this.session = new InferenceSession(model_path);
            this.threshold = threshold;
        }

        private DenseTensor<float> ArrayToDenseTensor(float[,] recording)
        {
            DenseTensor<float> to_ret = new DenseTensor<float>(new[] { 1, 677, 3 });
            for(int i = 0; i<recording.GetLength(0);i++)
            {
                for (int j = 0; j < recording.GetLength(1); j++)
                {
                    to_ret[0,i,j] = recording[i,j];
                }
            }
            return to_ret;
        }

        public float MakePrediction(float[,] recording)
        {
            if (recording.GetLength(0) != 677 || recording.GetLength(1) != 3)
                throw new ArgumentException("recording should be float[677,3]");
            DenseTensor<float> arr_as_tens = this.ArrayToDenseTensor(recording);
            var inputs = new List<NamedOnnxValue> { NamedOnnxValue.CreateFromTensor("modelInput", arr_as_tens) };
            var output = this.session.Run(inputs).First().AsTensor<float>();
            return output[0];
        }

        public bool AccidentOrNot(float[,] recording)
        {
            if (recording.GetLength(0) != 677 || recording.GetLength(1) != 3)
                throw new ArgumentException("recording should be float[677,3]");
            float prediction = this.MakePrediction(recording);
            return prediction >= this.threshold;
        }

        public bool AccidentOrNot(float prediction)
        {
            return prediction >= this.threshold;
        }
    }
}
