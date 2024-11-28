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

        private void button_change_Click(object sender, EventArgs e)
        {
            string pas = textBox_new_password.Text;

            using (StreamWriter w = new StreamWriter(@"change_mail_password.bat", false, Encoding.GetEncoding(1251)))//false - замена, true - дозапись
            {
                w.WriteLine("python change_mail_password.py " + pas);
                w.WriteLine("pause");
            }
            Process.Start("change_mail_password.bat");
            this.Close();
        }

        private void button_migrate_Click(object sender, EventArgs e)
        {
            Process.Start("migrate_server.bat");
        }
    }
}
