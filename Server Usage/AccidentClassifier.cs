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
        private DenseTensor<float> input_template = new DenseTensor<float>(new[] { 1, 677, 3 });
        private float threshold;

        public AccidentClassifier(string model_path, float threshold = 0.5f)
        {
            this.session = new InferenceSession(model_path);
            this.threshold = threshold;
        }

        public float MakePrediction(float[,,] recording)
        {
            if (recording.GetLength(0) != 1 || recording.GetLength(1) != 677 || recording.GetLength(2) != 3)
                throw new ArgumentException("recording should be float[1,677,3]");
            var inputs = new List<NamedOnnxValue> { NamedOnnxValue.CreateFromTensor("modelInput", this.input_template) };
            var output = this.session.Run(inputs).First().AsTensor<float>();
            return output[0];
        }

        public bool AccidentOrNot(float[,,] recording)
        {
            if (recording.GetLength(0) != 1 || recording.GetLength(1) != 677 || recording.GetLength(2) != 3)
                throw new ArgumentException("recording should be float[1,677,3]");
            float prediction = this.MakePrediction(recording);
            return prediction >= this.threshold;
        }

        public bool AccidentOrNot(float prediction)
        {
            return prediction >= this.threshold;
        }
    }
}
