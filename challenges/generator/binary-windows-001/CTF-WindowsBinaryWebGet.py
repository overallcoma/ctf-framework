import argparse
import subprocess
import os
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", dest="url", help="URL to query")
parser.add_argument("-rh1", "--redherring1", dest="redherring1", help="Red Herring 1 Value")
parser.add_argument("-rh2", "--redherring2", dest="redherring2", help="Red Herring 2 Value")
args = parser.parse_args()

if args.url is None:
    print("Please specify a target URL")
    exit(1)
else:
    target_url = args.url
if args.redherring1 is None:
    print("This challenge requires a Fake Flag/Red Herring")
    print("Please specify a Red Herring with -rh1")
    exit(1)
else:
    redherring1 = args.redherring1

if args.redherring2 is None:
    print("This challenge requires a Fake Flag/Red Herring")
    print("Please specify a Red Herring with -rh2")
    exit(1)
else:
    redherring2 = args.redherring2

form1cs_content = """using System;
using System.Net;
using System.Windows.Forms;
namespace WindowsFormsApp1
{{
    public partial class Owned : Form
    {{
        public Owned()
        {{
            string stuff1 = "{0}";
            string stuff2 = "{1}";
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create("{2}");
            HttpWebResponse response = (HttpWebResponse)request.GetResponse();
            InitializeComponent();
        }}      
        private void Form1_Load(object sender, EventArgs e)           
        {{
        }}
        private void button1_Click(object sender, EventArgs e)
        {{
            MessageBox.Show("Did you really think it was that easy?");
        }}
    }}
}}""".format(redherring1, redherring2, target_url)

try:
    os.remove("./formsapp/WindowsFormsApp1/Form1.cs")
except:
    print('')
formsave = open("./formsapp/WindowsFormsApp1/Form1.cs", "w+")
formsave.write(form1cs_content)
formsave.close()
os.chdir('./formsapp')
subprocess.call(['xbuild', './WindowsFormsApp1.sln'])
os.chdir('..')
shutil.move('./formsapp/WindowsFormsApp1/bin/Debug/WindowsFormsApp1.exe', './App.exe')
