using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using System.Threading;
using System.Diagnostics;
using System.Globalization;

namespace Starter
{

    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }
        private void Form1_Load(object sender, EventArgs e)
        {
            
        }
        public void button_Add_Click(object sender, EventArgs e)
        {           
            Process.Start("start_server.bat");
        }
        private void button_Quit_Click(object sender, EventArgs e)
        {
            Process.Start("start_bg_task.bat");
        }
    }
}
