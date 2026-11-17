
"""Main application window for LUCIFER."""

from PySide6.QtCore import (
    QEasingCurve,
    QParallelAnimationGroup,
    QPropertyAnimation,
    QSize,
    Qt,
)
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from lucifer.interface.components.orb import LuciferOrb
from lucifer.interface.components.sidebar import Sidebar
from lucifer.interface.components.task_panel import TaskPanel
from lucifer.interface.components.conversation_view import ConversationView
from lucifer.interface.components.chat_input import ChatInput
from lucifer.interface.styles.theme import build_stylesheet


class LuciferWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("LUCIFER")
        self.resize(1440, 900)
        self.setMinimumSize(1100, 700)

        self._text_mode = False
        self._mode_animation = None

        self._setup_ui()
        self.setStyleSheet(build_stylesheet())

    def _setup_ui(self) -> None:
        """Assemble the main application layout."""

        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)

        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(18)

        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # Central workspace
        self.workspace = QWidget()
        workspace_layout = QHBoxLayout(self.workspace)

        workspace_layout.setContentsMargins(12, 12, 12, 12)
        workspace_layout.setSpacing(20)

        # ----------------------------------
        # Orb panel
        # ----------------------------------

        self.orb_panel = QWidget()
        self.orb_panel.setMinimumWidth(220)
        self.orb_panel.setMaximumWidth(16777215)
        self.orb_panel.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.orb_layout = QVBoxLayout(self.orb_panel)
        self.orb_layout.setContentsMargins(0, 0, 0, 0)
        self.orb_layout.setSpacing(14)

        self.orb_layout.addStretch()

        self.orb = LuciferOrb()
        self.orb.setMinimumSize(160, 160)
        self.orb.setMaximumSize(420, 420)
        self.orb.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred,
        )

        self.orb_layout.addWidget(
            self.orb,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        self.orb_status = QLabel("SYSTEM STANDBY")
        self.orb_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.orb_status.setStyleSheet("""
            color: #718294;
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 2px;
        """)

        self.orb_layout.addWidget(self.orb_status)

        # Subtle voice transcript
        self.voice_transcript = QLabel("")
        self.voice_transcript.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.voice_transcript.setWordWrap(True)
        self.voice_transcript.setMaximumWidth(500)
        self.voice_transcript.setMinimumHeight(28)
        self.voice_transcript.setStyleSheet("""
            color: #8CA4B5;
            font-size: 12px;
            background: transparent;
        """)

        self.orb_layout.addWidget(
            self.voice_transcript,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        # Microphone button
        self.orbit_mic_button = QPushButton("MIC")
        self.orbit_mic_button.setFixedSize(76, 38)
        self.orbit_mic_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        self.orbit_mic_button.setToolTip(
            "Activate voice input"
        )
        self.orbit_mic_button.clicked.connect(
            self._handle_microphone_request
        )
        self.orbit_mic_button.setStyleSheet("""
            QPushButton {
                background: #172A38;
                color: #78CBE5;
                border: 1px solid #294455;
                border-radius: 9px;
                font-size: 11px;
                font-weight: 700;
            }

            QPushButton:hover {
                background: #203B4D;
                border: 1px solid #3B718A;
            }

            QPushButton:pressed {
                background: #28617A;
            }
        """)

        self.orb_layout.addWidget(
            self.orbit_mic_button,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        # Temporary orb state testing controls
        self.state_selector = QComboBox()
        self.state_selector.addItems([
            "Idle",
            "Listening",
            "Thinking",
            "Speaking",
            "Executing",
            "Error",
            "Offline",
        ])

        self.state_selector.currentTextChanged.connect(
            self._change_orb_state
        )

        self.orb_layout.addWidget(
            self.state_selector,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        # ----------------------------------
        # Conversation panel
        # ----------------------------------

        self.conversation_panel = QWidget()
        self.conversation_panel.setMinimumWidth(300)

        conversation_layout = QVBoxLayout(
            self.conversation_panel
        )

        conversation_layout.setContentsMargins(0, 0, 0, 0)
        conversation_layout.setSpacing(14)

        self.conversation_view = ConversationView()

        conversation_layout.addWidget(
            self.conversation_view,
            1,
        )

        # ----------------------------------
        # Shared chat input
        # ----------------------------------

        self.chat_input = ChatInput()

        self.chat_input.message_submitted.connect(
            self._handle_message
        )

        self.chat_input.microphone_requested.connect(
            self._handle_microphone_request
        )

        self.orb_layout.addWidget(self.chat_input)

        # Hidden until first typed message
        self.conversation_panel.hide()

        workspace_layout.addWidget(self.orb_panel, 1)
        workspace_layout.addWidget(
            self.conversation_panel,
            1,
        )

        main_layout.addWidget(self.workspace, 1)

        # Right task monitoring panel
        self.task_panel = TaskPanel()
        main_layout.addWidget(self.task_panel)

        self.setCentralWidget(central_widget)

    def _handle_message(self, message: str) -> None:
        """Handle manually submitted text messages."""

        if not self._text_mode:
            self._enter_text_mode()

        self.conversation_view.add_message(
            message,
            "user",
        )

        self.orb_status.setText("AI ENGINE NOT CONNECTED")

    def _enter_text_mode(self) -> None:
        """Move the orb left and reveal conversation history."""

        if self._text_mode:
            return

        self._text_mode = True

        # Capture the current dimensions.
        panel_start_width = self.orb_panel.width()
        orb_start_size = self.orb.size()

        # Move the shared chat input into the conversation panel.
        self.orb_layout.removeWidget(self.chat_input)

        conversation_layout = self.conversation_panel.layout()
        conversation_layout.addWidget(self.chat_input)

        # Reveal conversation history.
        self.conversation_panel.show()

        # Animate orb panel width.
        panel_animation = QPropertyAnimation(
            self.orb_panel,
            b"maximumWidth",
            self,
        )

        panel_animation.setDuration(600)
        panel_animation.setStartValue(panel_start_width)
        panel_animation.setEndValue(280)
        panel_animation.setEasingCurve(
            QEasingCurve.Type.InOutCubic
        )

        # Animate orb size.
        orb_animation = QPropertyAnimation(
            self.orb,
            b"maximumSize",
            self,
        )

        orb_animation.setDuration(600)
        orb_animation.setStartValue(orb_start_size)
        orb_animation.setEndValue(QSize(220, 220))
        orb_animation.setEasingCurve(
            QEasingCurve.Type.InOutCubic
        )

        animation_group = QParallelAnimationGroup(self)
        animation_group.addAnimation(panel_animation)
        animation_group.addAnimation(orb_animation)

        self._mode_animation = animation_group
        animation_group.start()

        self.chat_input.message_field.setFocus()

    def _handle_microphone_request(self) -> None:
        """Handle voice activation without changing layout."""

        self.orb_status.setText("VOICE INPUT NOT CONNECTED")

        self.orb.set_state("listening")

        self.voice_transcript.setText(
            "Voice interaction will be available soon."
        )

    def _change_orb_state(self, state: str) -> None:
        """Temporarily change the orb state for testing."""

        state_id = state.lower().strip()

        self.orb.set_state(state_id)
        self.orb_status.setText(state.upper())

    def show_orbit_mode(self) -> None:
        """Restore the centered orb interface."""

        if not self._text_mode:
            return

        self._text_mode = False

        if self._mode_animation:
            self._mode_animation.stop()

        # Move the shared input back under the orb.
        self.conversation_panel.layout().removeWidget(
            self.chat_input
        )

        self.orb_layout.addWidget(self.chat_input)

        self.conversation_panel.hide()

        self.orb_panel.setMaximumWidth(16777215)
        self.orb.setMinimumSize(160, 160)
        self.orb.setMaximumSize(420, 420)

        self.orb_status.setText("SYSTEM STANDBY")
        self.voice_transcript.clear()
