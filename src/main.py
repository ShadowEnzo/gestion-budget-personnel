# import sys
# from PySide6.QtWidgets import QApplication
# from model.dashboard_model import DashboardModel
# from view.dashboard_view import DashboardView
# from controller.dashboard_controller import DashboardController

# if __name__ == "__main__":
#     app = QApplication([])
#     # app.setStyleSheet("""
#     #     QWidget {
#     #         background-color: #f5f6fa;
#     #         font-family: Arial;
#     #         font-size: 15px;
#     #     }
#     #     QLabel {
#     #         color: #222f3e;
#     #         font-weight: bold;
#     #     }
#     #     QPushButton {
#     #         background-color: #54a0ff;
#     #         color: white;
#     #         border-radius: 8px;
#     #         padding: 8px 16px;
#     #     }
#     #     QPushButton:hover {
#     #         background-color: #2e86de;
#     #     }
#     #     QListWidget {
#     #         background: #fff;
#     #         border: 1px solid #dfe4ea;
#     #         border-radius: 6px;
#     #     }
#     # """)
#     model = DashboardModel()
#     view = DashboardView()
#     controller = DashboardController(model, view)
#     view.resize(800, 600)
#     view.show()
#     sys.exit(app.exec())
