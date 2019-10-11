using System;
using System.Net;
using System.Windows.Forms;

namespace WindowsFormsApp1
{
    public partial class Owned : Form
    {
        public Owned()
        {
            string stuff1 = "Load random shit but not your FLAG";
            uint stuff2 = 3252535434;
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create("https://stevenloftus.com");
            HttpWebResponse response = (HttpWebResponse)request.GetResponse();

            InitializeComponent();

        }      
        private void Form1_Load(object sender, EventArgs e)
           
        {
                       

        }

        private void button1_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Did you really think it was that easy?");
        }
    }
}
