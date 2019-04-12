using System;
using System.IO;
using ThorlabsKDC101Server;

namespace ThorlabsKDC101ServerCLI
{
    public class Program
    {
        static private ThorlabsKDC101Server.ThorlabsKDC101Server _Server = null;
        static void Main(string[] args)
        {
            int Port = 50052;
            bool Debug = true;


            if (args.Length > 0)
            {
                Int32.TryParse(args[0], out Port);
            }
            if (args.Length > 1)
            {
                bool.TryParse(args[1], out Debug);
            }

            _Server = new ThorlabsKDC101Server.ThorlabsKDC101Server();
            _Server.StartServing("localhost", Port);
            
            Console.WriteLine("KDC101 device server listening on port " + Port);
            Console.WriteLine("Press any key to stop the server...");
            Console.ReadKey();
            
            _Server.StopServing();

        }
    }
}
