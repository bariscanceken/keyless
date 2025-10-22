import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets


class CyberpunkWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("keyless")
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowCloseButtonHint)

        # Logo referansını erken başlat (resizeEvent sırasında güvenlik)
        self.logo_label = None

        # Tam ekran
        self.showMaximized()
        
        # Ekran boyutunu al ve tam ekran yap
        screen = QtWidgets.QApplication.primaryScreen()
        if screen:
            geometry = screen.availableGeometry()
            self.setGeometry(geometry)

        # Merkezi widget oluştur
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # UI bileşenleri
        self._build_ui(central_widget)

        # Tema uygula
        self._apply_theme()
        
        # ESC tuşu ile kapatma
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        super().keyPressEvent(event)

    def _build_ui(self, parent):
        # Ana layout - merkezi hizalama
        main_layout = QtWidgets.QVBoxLayout(parent)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(40)
        
        # Üst boşluk
        main_layout.addStretch(2)
        
        # Sol logo alanı
        self.logo_label = QtWidgets.QLabel()
        self.logo_label.setObjectName("LogoLabel")
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)
        self.logo_label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # Merkezi kart widget
        card_widget = QtWidgets.QWidget()
        card_widget.setObjectName("CardWidget")
        card_layout = QtWidgets.QVBoxLayout(card_widget)
        card_layout.setContentsMargins(60, 60, 60, 60)
        card_layout.setSpacing(30)
        
        # Başlık
        title = QtWidgets.QLabel("KEYLESS")
        title.setObjectName("Title")
        title.setAlignment(QtCore.Qt.AlignCenter)
        card_layout.addWidget(title)
        
        # Boşluk
        card_layout.addSpacing(20)
        
        # Dosya seçme bölümü
        file_section = QtWidgets.QVBoxLayout()
        file_section.setSpacing(15)
        
        file_label = QtWidgets.QLabel("Vault File")
        file_label.setObjectName("FieldLabel")
        file_section.addWidget(file_label)
        
        file_row = QtWidgets.QHBoxLayout()
        file_row.setSpacing(15)
        self.file_line = QtWidgets.QLineEdit()
        self.file_line.setReadOnly(True)
        self.file_line.setPlaceholderText("No vault file selected")
        self.file_line.setObjectName("FileInput")
        browse_btn = QtWidgets.QPushButton("Browse")
        browse_btn.setObjectName("BrowseButton")
        browse_btn.clicked.connect(self._choose_file)
        browse_btn.enterEvent = lambda event: self._button_hover_enter(browse_btn)
        browse_btn.leaveEvent = lambda event: self._button_hover_leave(browse_btn)
        file_row.addWidget(self.file_line, 1)
        file_row.addWidget(browse_btn, 0)
        file_section.addLayout(file_row)
        
        card_layout.addLayout(file_section)
        
        # Şifre bölümü
        pass_section = QtWidgets.QVBoxLayout()
        pass_section.setSpacing(15)
        
        pass_label = QtWidgets.QLabel("Password")
        pass_label.setObjectName("FieldLabel")
        pass_section.addWidget(pass_label)
        
        pass_row = QtWidgets.QHBoxLayout()
        pass_row.setSpacing(15)
        self.pass_edit = QtWidgets.QLineEdit()
        self.pass_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_edit.setPlaceholderText("Enter your password")
        self.pass_edit.setObjectName("PasswordInput")
        toggle_btn = QtWidgets.QPushButton("👁")
        toggle_btn.setObjectName("ToggleButton")
        toggle_btn.setCheckable(True)
        toggle_btn.setToolTip("Show/Hide password")
        toggle_btn.toggled.connect(self._toggle_password)
        toggle_btn.enterEvent = lambda event: self._button_hover_enter(toggle_btn)
        toggle_btn.leaveEvent = lambda event: self._button_hover_leave(toggle_btn)
        pass_row.addWidget(self.pass_edit, 1)
        pass_row.addWidget(toggle_btn, 0)
        pass_section.addLayout(pass_row)
        
        card_layout.addLayout(pass_section)
        
        # Boşluk
        card_layout.addSpacing(30)
        
        # Login butonu
        self.login_btn = QtWidgets.QPushButton("ACCESS VAULT")
        self.login_btn.setObjectName("LoginButton")
        self.login_btn.clicked.connect(self._on_login)
        self.login_btn.enterEvent = lambda event: self._button_hover_enter(self.login_btn)
        self.login_btn.leaveEvent = lambda event: self._button_hover_leave(self.login_btn)
        card_layout.addWidget(self.login_btn)
        
        # Kartı sağa, logoyu sola yerleştir
        card_container = QtWidgets.QHBoxLayout()
        # Sol: logo (daha büyük alan)
        card_container.addStretch(1)
        card_container.addWidget(self.logo_label, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        card_container.addSpacing(100)
        # Sağ: form kartı (ekranın sağına)
        card_container.addWidget(card_widget, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        card_container.addStretch(1)
        
        main_layout.addLayout(card_container)
        
        # Alt boşluk
        main_layout.addStretch(2)

        # Logo yükle ve ölçekle
        self._load_logo()
        self._scale_logo()

    def _apply_theme(self):
        # Neon cyberpunk renk paleti (sarı-mor)
        palette_bg = "#0a0a0a"      # koyu siyah
        palette_panel = "#1a0f1a"   # koyu mor panel
        neon_primary = "#ffdd00"    # neon sarı
        neon_secondary = "#aa44ff"  # neon mor
        text_color = "#f0f0f0"

        qss = f"""
        QMainWindow {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {palette_bg}, stop:1 #1a1a1a);
        }}
        QWidget {{
            background: transparent;
            color: {text_color};
            font-family: 'Segoe UI', 'Consolas', monospace;
        }}
        #LogoLabel {{
            background: transparent;
        }}
        #CardWidget {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {palette_panel}, stop:1 #2a1f2a);
            border: 2px solid {neon_primary}33;
            border-radius: 20px;
            min-width: 500px;
            min-height: 400px;
        }}
        #Title {{
            color: {neon_primary};
            font-size: 36px;
            font-weight: 800;
            letter-spacing: 3px;
            margin-bottom: 10px;
        }}
        #Subtitle {{
            color: {neon_secondary};
            font-size: 16px;
            font-weight: 300;
            letter-spacing: 1px;
            margin-bottom: 20px;
        }}
        #FieldLabel {{
            color: {text_color};
            font-size: 18px;
            font-weight: 600;
            letter-spacing: 1px;
        }}
        QLineEdit {{
            background: rgba(26, 15, 26, 0.8);
            border: 2px solid {neon_primary}22;
            border-radius: 12px;
            padding: 15px 20px;
            font-size: 16px;
            selection-background-color: {neon_secondary}55;
        }}
        QLineEdit:focus {{
            border: 2px solid {neon_primary};
            box-shadow: 0 0 20px {neon_primary}44;
        }}
        QPushButton {{
            background: transparent;
            border: 2px solid {neon_primary}33;
            color: {text_color};
            padding: 15px 25px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            letter-spacing: 1px;
        }}
        #LoginButton {{
            font-size: 20px;
            padding: 20px 40px;
            border-radius: 15px;
            letter-spacing: 2px;
        }}
        #BrowseButton, #ToggleButton {{
            min-width: 120px;
            font-size: 14px;
        }}
        QToolTip {{
            background: {palette_panel};
            color: {text_color};
            border: 1px solid {neon_secondary};
            font-size: 12px;
        }}
        """
        self.setStyleSheet(qss)
        
        # Stil güncellemesini zorla
        self.style().unpolish(self)
        self.style().polish(self)

        # Çok hafif neon parıltılı gölge
        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setColor(QtGui.QColor(neon_primary))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)


    def _load_logo(self):
        # Çalışma dizininde logo dosyasını ara
        candidates = [
            "logo.png",
            os.path.join(os.getcwd(), "logo.png"),
        ]
        logo_path = None
        for c in candidates:
            if os.path.isfile(c):
                logo_path = c
                break
        if not logo_path:
            # Bulunamazsa gizle
            self.logo_label.hide()
            return

        pixmap = QtGui.QPixmap(logo_path)
        if pixmap.isNull():
            self.logo_label.hide()
            return
        self.logo_label.setPixmap(pixmap)
        self.logo_label.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # logo_label henüz oluşturulmamış olabilir
        if hasattr(self, "logo_label") and isinstance(self.logo_label, QtWidgets.QLabel) and self.logo_label is not None:
            self._scale_logo()

    def _scale_logo(self):
        if not hasattr(self, "logo_label") or not isinstance(self.logo_label, QtWidgets.QLabel) or self.logo_label is None:
            return
        if not self.logo_label.pixmap():
            return
        
        # Konteyner boyutunu al (min-width: 500px, min-height: 400px)
        container_w = max(500, int(self.width() * 0.3))
        container_h = max(400, int(self.height() * 0.5))
        
        # Logoyu konteyner ile aynı boyutta ölçekle
        scaled = self.logo_label.pixmap().scaled(
            container_w,
            container_h,
            QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation,
        )
        self.logo_label.setPixmap(scaled)

    def _button_hover_enter(self, button):
        if button.objectName() == "LoginButton":
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 221, 0, 0.4);
                    border: 2px solid #ffdd00;
                    color: #0a0a0a;
                    padding: 20px 40px;
                    border-radius: 15px;
                    font-size: 20px;
                    font-weight: 600;
                    letter-spacing: 2px;
                }
            """)
        else:
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 221, 0, 0.3);
                    border: 2px solid #ffdd00;
                    color: #0a0a0a;
                    padding: 15px 25px;
                    border-radius: 12px;
                    font-size: 16px;
                    font-weight: 600;
                    letter-spacing: 1px;
                }
            """)

    def _button_hover_leave(self, button):
        if button.objectName() == "LoginButton":
            button.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: 2px solid rgba(255, 221, 0, 0.2);
                    color: #f0f0f0;
                    padding: 20px 40px;
                    border-radius: 15px;
                    font-size: 20px;
                    font-weight: 600;
                    letter-spacing: 2px;
                }
            """)
        else:
            button.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: 2px solid rgba(255, 221, 0, 0.2);
                    color: #f0f0f0;
                    padding: 15px 25px;
                    border-radius: 12px;
                    font-size: 16px;
                    font-weight: 600;
                    letter-spacing: 1px;
                }
            """)

    def _choose_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select Vault File",
            "",
            "Vault Files (*.vault);;All Files (*)"
        )
        if path:
            # Güvenli dosya yolu kontrolü
            try:
                # Mutlak yolu al
                abs_path = os.path.abspath(path)
                # Dosya var mı kontrol et
                if os.path.isfile(abs_path):
                    self.file_line.setText(abs_path)
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", "Selected file does not exist.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Invalid file path: {str(e)}")

    def _toggle_password(self, checked: bool):
        self.pass_edit.setEchoMode(
            QtWidgets.QLineEdit.Normal if checked else QtWidgets.QLineEdit.Password
        )

    def _on_login(self):
        file_path = self.file_line.text().strip()
        
        # Güvenli şifre temizleme için bytearray kullan
        password_bytes = None
        try:
            # Ara değişken olmadan direkt bytearray'e çevir
            password_bytes = bytearray(self.pass_edit.text().encode('utf-8'))
            
            if not file_path:
                QtWidgets.QMessageBox.warning(self, "Warning", "Please select a vault file.")
                return
            if not password_bytes:
                QtWidgets.QMessageBox.warning(self, "Warning", "Please enter password.")
                return
            
            # Dosya yolunu doğrula
            if not os.path.isfile(file_path):
                QtWidgets.QMessageBox.warning(self, "Error", "Selected file does not exist.")
                return
            
            # Demo için başarılı giriş
            QtWidgets.QMessageBox.information(self, "Success", "Login successful! (Demo)")
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
        finally:
            # Güvenli şifre temizleme
            if password_bytes:
                password_bytes[:] = b'\x00' * len(password_bytes)
                del password_bytes
            # UI'dan şifreyi temizle
            self.pass_edit.clear()

def screen():
    app = QtWidgets.QApplication(sys.argv)
    win = CyberpunkWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    screen()