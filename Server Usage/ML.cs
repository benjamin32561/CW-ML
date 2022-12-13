using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;



namespace Server_Usage
{
    internal class Program
    {
        static void Main(string[] args)
        {
            string modelFilePath = "C:\\Users\\ben32\\Desktop\\Work\\Cloud-Wise-ML\\Server Usage\\model.onnx";

            AccidentClassifier model = new AccidentClassifier(modelFilePath);

            float[,] test = new float[677, 3];
            Console.WriteLine(model.MakePrediction(test));
            Console.WriteLine(model.AccidentOrNot(test));
        }
    }
}
