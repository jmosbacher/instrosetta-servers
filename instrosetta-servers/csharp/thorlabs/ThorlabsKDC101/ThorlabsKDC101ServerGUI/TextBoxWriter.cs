using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Windows.Controls;

namespace ThorlabsKDC101ServerGUI
{
    public class TextBoxWriter : TextWriter
    {
        private TextBlock textbox;
        public TextBoxWriter(TextBlock textbox)
        {
            this.textbox = textbox;
        }

        public override void Write(char value)
        {
            textbox.Text += value;
        }
        
        public override void Write(string value)
        {
            textbox.Text += value;
        }

        public override Encoding Encoding
        {
            get { return Encoding.Unicode; }
        }
    }
}
