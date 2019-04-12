using System;
using System.Text.RegularExpressions;
using System.Windows;
using System.Windows.Input;
using ThorlabsKDC101Server;

namespace ThorlabsKDC101ServerGUI
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private bool _Serving = false;
        private ThorlabsKDC101Server.ThorlabsKDC101Server _Server = new ThorlabsKDC101Server.ThorlabsKDC101Server();
  
        private bool _IncludeSims = false;

        public MainWindow()
        {
            InitializeComponent();
        }



            private void StartStopServeButton_Click(object sender, RoutedEventArgs e)
        {
            if (_Serving)
            {
                _Server.StopServing();
                _Serving = false;
                ServingCheckBox.IsChecked = false;
                StartStopServeButton.Content = "Serve";
                LogPreview.Text += "\nStoped.";

            } else
            {
                LogPreview.Text = "Starting device server...";
                TextBoxWriter text_writer = new TextBoxWriter(LogPreview);
                Console.SetOut(text_writer);
                _Server.StartServing(ServeAddressInput.Text, int.Parse(ServePortInput.Text));
                _Serving = true;
                ServingCheckBox.IsChecked = true;
                StartStopServeButton.Content = "Stop";
                LogPreview.Text += System.String.Format( "\nDevice server running on {0}:{1}.", ServeAddressInput.Text, int.Parse(ServePortInput.Text));
            }

        }

        private void IncludeSimulated_Changed(object sender, RoutedEventArgs e)
        {
            _IncludeSims = (bool)IncludeSimulated.IsChecked;
        }


        private static readonly Regex _regex = new Regex("[^0-9.-]+"); //regex that matches disallowed text
        private static bool IsTextAllowed(string text)
        {
            return !_regex.IsMatch(text);
        }



        private void ServePortInput_Pasting(object sender, DataObjectPastingEventArgs e)
        {
            if (e.DataObject.GetDataPresent(typeof(String)))
            {
                String text = (String)e.DataObject.GetData(typeof(String));
                if (!IsTextAllowed(text))
                {
                    e.CancelCommand();
                }
            }
            else
            {
                e.CancelCommand();
            }
        }

        private void ServePortInput_Preview(object sender, TextCompositionEventArgs e)
        {
            e.Handled = !IsTextAllowed(e.Text);
        }

    }
}
