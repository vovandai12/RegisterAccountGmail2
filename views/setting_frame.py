import tkinter as tk
from config import (
    TMPROXY,
    PROXYSHOPLIKE,
    PROXYFB,
    BOSSOTP,
    IRONSIM,
    VIOTP,
    SIMOTP,
    HCOTP,
)
import config as config
from config import WriteConfig


class SettingFrame(tk.Frame):
    def __init__(self, master, window, cnf={}, **kwargs):
        tk.Frame.__init__(self, master, **kwargs, bg="white")
        self.window = window
        lb_proxy = self.Lb_proxy()
        lb_otp = self.Lb_otp()
        lb_profile = self.Lb_profile()
        lb_system = self.Lb_system()
        button_start, button_stop, button_format = self.Bt_action()
        lb_proxy.grid(row=0, column=0, padx=(5), pady=(5), sticky=tk.NSEW)
        lb_otp.grid(row=1, column=0, padx=(5), pady=(5), sticky=tk.NSEW)
        lb_profile.grid(row=2, column=0, padx=(5), pady=(5), sticky=tk.NSEW)
        lb_system.grid(row=3, column=0, padx=(5), pady=(5), sticky=tk.NSEW)
        button_start.grid(row=4, column=0, padx=5, pady=5, sticky=tk.N + tk.W)
        button_stop.grid(row=4, column=0, padx=130, pady=5, sticky=tk.N + tk.W)
        button_format.grid(row=4, column=0, padx=260, pady=5, sticky=tk.N + tk.W)

    def Lb_proxy(self):
        lb = tk.LabelFrame(self, text="Proxy", bg="white")
        lba_proxy = tk.Label(lb, text="Dịch vụ proxy:", bg="white")
        options_proxy = [TMPROXY, PROXYSHOPLIKE, PROXYFB]
        variable_proxy = tk.StringVar()
        variable_proxy.set(config.global_config.methodProxy)

        def command_proxy(value):
            config.global_config.methodProxy = value
            WriteConfig(config.global_config)

        menu_proxy = tk.OptionMenu(
            lb,
            variable_proxy,
            *options_proxy,
            command=command_proxy,
        )
        menu_proxy.config(width=53)
        lba_key = tk.Label(lb, text="Key proxy:", bg="white")
        value_keyProxy = config.global_config.keyProxy
        text_key = tk.Text(lb, borderwidth=1, relief="solid")
        text_key.delete("1.0", "end")
        text_key.delete("1.0", "end")
        if not value_keyProxy is None:
            for item in value_keyProxy:
                text_key.insert("1.0", item + "\n")
        text_key.bind(
            "<KeyRelease>",
            lambda event: creator_text_proxy(
                "keyProxy", text_key.get("1.0", "end-1c").splitlines()
            ),
        )
        text_key.config(width=40, height=5)

        lba_proxy.grid(row=0, column=0, sticky=tk.W + tk.E, padx=5, pady=5)
        menu_proxy.grid(row=0, column=1, sticky=tk.W + tk.E, padx=5, pady=5)
        lba_key.grid(row=1, column=0, sticky=tk.W + tk.E, padx=5, pady=5)
        text_key.grid(row=1, column=1, sticky=tk.W + tk.E, padx=5, pady=5)
        return lb

    def Lb_otp(self):
        lb = tk.LabelFrame(self, text="Số điện thoại", bg="white")
        lba_otp = tk.Label(lb, text="Dịch vụ otp:", bg="white")
        options_otp = [BOSSOTP, IRONSIM, VIOTP, SIMOTP, HCOTP]
        variable_otp = tk.StringVar()
        variable_otp.set(config.global_config.methodOtp)

        def command_otp(value):
            config.global_config.methodOtp = value
            WriteConfig(config.global_config)

        menu_otp = tk.OptionMenu(
            lb,
            variable_otp,
            *options_otp,
            command=command_otp,
        )
        menu_otp.config(width=53)
        lba_key = tk.Label(lb, text="Key otp:", bg="white")
        default_otp_key = tk.StringVar()
        default_otp_key.set(config.global_config.keyOtp)
        entry_key_otp = tk.Entry(
            lb, textvariable=default_otp_key, borderwidth=1, relief="solid"
        )
        entry_key_otp.config(
            width=55,
            validate="key",
            validatecommand=(lb.register(creator("keyOtp")), "%P"),
        )

        lba_otp.grid(row=0, column=0, sticky=tk.W + tk.E, padx=5, pady=5)
        menu_otp.grid(row=0, column=1, sticky=tk.W + tk.E, padx=5, pady=5)
        lba_key.grid(row=1, column=0, sticky=tk.W + tk.E, padx=5, pady=5)
        entry_key_otp.grid(row=1, column=1, sticky=tk.W + tk.E, padx=5, pady=5)
        return lb

    def Lb_profile(self):
        lb = tk.LabelFrame(self, text="Thông tin tài khoản", bg="white")
        label_password = tk.Label(lb, text="Mật khẩu:", bg="white")
        default_password = tk.StringVar()
        default_password.set(config.global_config.defaultPassword)
        entry_password = tk.Entry(
            lb, textvariable=default_password, borderwidth=1, relief="solid"
        )
        selected_password = tk.StringVar()
        selected_password.set(config.global_config.randomPassword)

        def command_random_password():
            config.global_config.randomPassword = selected_password.get()
            WriteConfig(config.global_config)

        check_passwrod = tk.Checkbutton(
            lb,
            text="Ngẫu nhiên",
            command=command_random_password,
            variable=selected_password,
            onvalue="agree",
            offvalue="disagree",
            bg="white",
        )
        label_fullName = tk.Label(lb, text="Họ và tên:", bg="white")
        selected_fullName = tk.StringVar()
        selected_fullName.set(config.global_config.fullName)
        radio_fullName_US = tk.Radiobutton(
            lb,
            text="US Ngẫu nhiên",
            variable=selected_fullName,
            value="US",
            bg="white",
        )
        radio_fullName_VN = tk.Radiobutton(
            lb,
            text="VN Ngẫu nhiên",
            variable=selected_fullName,
            value="VN",
            bg="white",
        )
        label_gender = tk.Label(lb, text="Giới tính:", bg="white")
        selected_gender = tk.StringVar()
        selected_gender.set(config.global_config.gender)
        radio_male = tk.Radiobutton(
            lb,
            text="Nam",
            variable=selected_gender,
            value="male",
            bg="white",
        )
        radio_female = tk.Radiobutton(
            lb,
            text="Nữ",
            variable=selected_gender,
            value="female",
            bg="white",
        )
        radio_random = tk.Radiobutton(
            lb,
            text="Ngẫu nhiên",
            variable=selected_gender,
            value="random",
            bg="white",
        )
        entry_password.config(
            width=45,
            validate="key",
            validatecommand=(lb.register(creator("defaultPassword")), "%P"),
        )
        radio_fullName_US.config(
            anchor=tk.W,
            justify=tk.LEFT,
            command=lambda: creator_radio("fullName", selected_fullName.get()),
        )
        radio_fullName_VN.config(
            anchor=tk.W,
            justify=tk.LEFT,
            command=lambda: creator_radio("fullName", selected_fullName.get()),
        )
        radio_male.config(
            anchor=tk.W,
            justify=tk.LEFT,
            command=lambda: creator_radio("gender", selected_gender.get()),
        )
        radio_female.config(
            anchor=tk.W,
            justify=tk.LEFT,
            command=lambda: creator_radio("gender", selected_gender.get()),
        )
        radio_random.config(
            anchor=tk.W,
            justify=tk.LEFT,
            command=lambda: creator_radio("gender", selected_gender.get()),
        )
        label_recovery = tk.Label(lb, text="Mail kp:", bg="white")
        default_recovery = tk.StringVar()
        default_recovery.set(config.global_config.fileRecovery)
        entry_recovery = tk.Entry(
            lb, textvariable=default_recovery, borderwidth=1, relief="solid"
        )
        entry_recovery.config(
            width=60,
            validate="key",
            validatecommand=(lb.register(creator("fileRecovery")), "%P"),
        )
        label_password.grid(
            row=0,
            column=0,
            sticky=tk.W + tk.E,
            padx=5,
            pady=5,
        )
        entry_password.grid(
            row=0,
            column=1,
            columnspan=2,
            sticky=tk.N + tk.W,
            padx=5,
            pady=5,
        )
        check_passwrod.grid(
            row=0,
            column=3,
            sticky=tk.N + tk.W,
            padx=5,
            pady=5,
        )
        label_fullName.grid(
            row=1,
            column=0,
            sticky=tk.W + tk.E,
            padx=5,
            pady=5,
        )
        radio_fullName_US.grid(
            row=1,
            column=1,
            sticky=tk.N + tk.W,
            padx=5,
            pady=5,
        )
        radio_fullName_VN.grid(
            row=1,
            column=2,
            sticky=tk.N + tk.W,
            padx=5,
            pady=5,
        )
        label_gender.grid(
            row=2,
            column=0,
            sticky=tk.W + tk.E,
            padx=5,
            pady=5,
        )
        radio_male.grid(
            row=2,
            column=1,
            sticky=tk.N + tk.W,
            padx=5,
            pady=5,
        )
        radio_female.grid(
            row=2,
            column=2,
            sticky=tk.N + tk.W,
            padx=5,
            pady=5,
        )
        radio_random.grid(
            row=2,
            column=3,
            sticky=tk.N + tk.W,
            padx=5,
            pady=5,
        )
        label_recovery.grid(
            row=3,
            column=0,
            sticky=tk.N + tk.W,
            padx=5,
            pady=5,
        )
        entry_recovery.grid(
            row=3,
            column=1,
            columnspan=3,
            sticky=tk.N + tk.W,
            padx=5,
            pady=5,
        )
        return lb

    def Lb_system(self):
        lb = tk.LabelFrame(self, text="Cấu hình chung", bg="white")
        label_number_col = tk.Label(lb, text="Số hàng:", bg="white")
        variable_number_col = tk.StringVar()
        variable_number_col.set(config.global_config.numberCol)

        def on_number_col(event):
            value = spin_number_col.get()
            try:
                value = int(value)
                if value < 0:
                    value = 1
                    spin_number_col.delete(0, "end")
                    spin_number_col.insert(0, 1)
                elif value > 10:
                    value = 10
                    spin_number_col.delete(0, "end")
                    spin_number_col.insert(0, 10)
            except ValueError:
                value = 1
                spin_number_col.delete(0, "end")
                spin_number_col.insert(0, 1)
            config.global_config.numberCol = value
            WriteConfig(config.global_config)

        spin_number_col = tk.Spinbox(
            lb,
            from_=0,
            to=10,
            textvariable=variable_number_col,
            wrap=True,
        )
        spin_number_col.bind("<FocusOut>", on_number_col)
        spin_number_col.config(width=10, justify=tk.LEFT)
        label_account = tk.Label(lb, text="Tổng acc:", bg="white")
        variable_acc = tk.StringVar()
        variable_acc.set(config.global_config.numberAccount)

        def on_spinbox_acc(event):
            value = spin_acc.get()
            try:
                value = int(value)
                if value < 0:
                    value = 1000
                    spin_acc.delete(0, "end")
                    spin_acc.insert(0, 1000)
                elif value > 2000:
                    value = 2000
                    spin_acc.delete(0, "end")
                    spin_acc.insert(0, 2000)
            except ValueError:
                value = 1000
                spin_acc.delete(0, "end")
                spin_acc.insert(0, 1000)
            config.global_config.numberAccount = value
            WriteConfig(config.global_config)

        spin_acc = tk.Spinbox(
            lb,
            from_=0,
            to=2000,
            textvariable=variable_acc,
            wrap=True,
        )
        spin_acc.bind("<FocusOut>", on_spinbox_acc)
        spin_acc.config(width=10, justify=tk.LEFT)
        label_thread = tk.Label(lb, text="Số luồng:", bg="white")
        variable_thread = tk.StringVar()
        variable_thread.set(config.global_config.numberThread)

        def on_spinbox_thread(event):
            value = spin_thread.get()
            try:
                value = int(value)
                if value < 0:
                    value = 1
                    spin_thread.delete(0, "end")
                    spin_thread.insert(0, 1)
                elif value > 20:
                    value = 20
                    spin_thread.delete(0, "end")
                    spin_thread.insert(0, 20)
            except ValueError:
                value = 1
                spin_thread.delete(0, "end")
                spin_thread.insert(0, 1)
            config.global_config.numberThread = value
            WriteConfig(config.global_config)

        spin_thread = tk.Spinbox(
            lb,
            from_=0,
            to=20,
            textvariable=variable_thread,
            wrap=True,
        )
        spin_thread.bind("<FocusOut>", on_spinbox_thread)
        spin_thread.config(width=10, justify=tk.LEFT)

        label_number_col.grid(row=0, column=0, sticky=tk.W + tk.E, padx=5, pady=5)
        spin_number_col.grid(row=0, column=1, sticky=tk.W + tk.E, padx=5, pady=5)
        label_account.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W + tk.E)
        spin_acc.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W + tk.E)
        label_thread.grid(row=0, column=4, padx=5, pady=5, sticky=tk.W + tk.E)
        spin_thread.grid(row=0, column=5, padx=5, pady=5, sticky=tk.W + tk.E)
        return lb

    def Bt_action(self):
        button_start = tk.Button(
            self,
            cursor="hand2",
            text="BẮT ĐẦU",
            width=15,
            height=3,
            compound=tk.LEFT,
            foreground="white",
            bg="green",
            command=lambda: self.start(),
        )
        button_stop = tk.Button(
            self,
            cursor="hand2",
            text="KẾT THÚC",
            width=15,
            height=3,
            compound=tk.LEFT,
            foreground="white",
            bg="red",
            command=lambda: self.stop(),
        )
        button_format = tk.Button(
            self,
            cursor="hand2",
            text="GMAIL",
            width=15,
            height=3,
            compound=tk.LEFT,
            foreground="black",
            bg="white",
            command=lambda: self.gmail(),
        )
        return button_start, button_stop, button_format

    def start(self):
        try:
            self.window.start_callback()
            return
        except:
            return

    def stop(self):
        try:
            self.window.stop_callback()
            return
        except:
            return

    def gmail(self):
        try:
            self.window.format_callback()
            return
        except:
            return


def creator_text_proxy(attr_name, value):
    if value != getattr(config.global_config, attr_name):
        setattr(config.global_config, attr_name, value)
        WriteConfig(config.global_config)
    return True


def creator(attr_name):
    def validate_cmd(value):
        if value != getattr(config.global_config, attr_name):
            setattr(config.global_config, attr_name, value)
            WriteConfig(config.global_config)
        return True

    return validate_cmd


def creator_radio(attr_name, value):
    if value != getattr(config.global_config, attr_name):
        setattr(config.global_config, attr_name, value)
        WriteConfig(config.global_config)
    return True
