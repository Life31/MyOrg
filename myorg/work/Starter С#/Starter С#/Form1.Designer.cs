namespace Starter
{
    partial class Form1
    {
        /// <summary>
        /// Обязательная переменная конструктора.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Освободить все используемые ресурсы.
        /// </summary>
        /// <param name="disposing">истинно, если управляемый ресурс должен быть удален; иначе ложно.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Код, автоматически созданный конструктором форм Windows

        /// <summary>
        /// Требуемый метод для поддержки конструктора — не изменяйте 
        /// содержимое этого метода с помощью редактора кода.
        /// </summary>
        private void InitializeComponent()
        {
            this.button_Add = new System.Windows.Forms.Button();
            this.button_Quit = new System.Windows.Forms.Button();
            this.button_change = new System.Windows.Forms.Button();
            this.textBox_new_password = new System.Windows.Forms.TextBox();
            this.button_migrate = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // button_Add
            // 
            this.button_Add.Location = new System.Drawing.Point(15, 12);
            this.button_Add.Name = "button_Add";
            this.button_Add.Size = new System.Drawing.Size(196, 29);
            this.button_Add.TabIndex = 2;
            this.button_Add.Text = "Запуск сервера";
            this.button_Add.UseVisualStyleBackColor = true;
            this.button_Add.Click += new System.EventHandler(this.button_Add_Click);
            // 
            // button_Quit
            // 
            this.button_Quit.Location = new System.Drawing.Point(217, 12);
            this.button_Quit.Name = "button_Quit";
            this.button_Quit.Size = new System.Drawing.Size(196, 29);
            this.button_Quit.TabIndex = 3;
            this.button_Quit.Text = "Запуск мониторинга питания";
            this.button_Quit.UseVisualStyleBackColor = true;
            this.button_Quit.Click += new System.EventHandler(this.button_Quit_Click);
            // 
            // button_change
            // 
            this.button_change.Location = new System.Drawing.Point(15, 47);
            this.button_change.Name = "button_change";
            this.button_change.Size = new System.Drawing.Size(196, 29);
            this.button_change.TabIndex = 4;
            this.button_change.Text = "Сменить пароль";
            this.button_change.UseVisualStyleBackColor = true;
            this.button_change.Click += new System.EventHandler(this.button_change_Click);
            // 
            // textBox_new_password
            // 
            this.textBox_new_password.Location = new System.Drawing.Point(217, 47);
            this.textBox_new_password.Multiline = true;
            this.textBox_new_password.Name = "textBox_new_password";
            this.textBox_new_password.Size = new System.Drawing.Size(196, 29);
            this.textBox_new_password.TabIndex = 5;
            this.textBox_new_password.Text = "Новый пароль для почты";
            // 
            // button_migrate
            // 
            this.button_migrate.Location = new System.Drawing.Point(15, 82);
            this.button_migrate.Name = "button_migrate";
            this.button_migrate.Size = new System.Drawing.Size(196, 29);
            this.button_migrate.TabIndex = 6;
            this.button_migrate.Text = "Запуск миграций изменений";
            this.button_migrate.UseVisualStyleBackColor = true;
            this.button_migrate.Click += new System.EventHandler(this.button_migrate_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(418, 126);
            this.Controls.Add(this.button_migrate);
            this.Controls.Add(this.textBox_new_password);
            this.Controls.Add(this.button_change);
            this.Controls.Add(this.button_Quit);
            this.Controls.Add(this.button_Add);
            this.Name = "Form1";
            this.Text = "Ресурс учета заявок";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.Button button_Add;
        private System.Windows.Forms.Button button_Quit;
        private System.Windows.Forms.Button button_change;
        private System.Windows.Forms.TextBox textBox_new_password;
        private System.Windows.Forms.Button button_migrate;
    }
}

