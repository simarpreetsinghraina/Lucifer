
"""Live system monitoring component for LUCIFER."""

from pathlib import Path

import psutil
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class SystemVitals(QWidget):
    """Display live hardware and system metrics."""

    def __init__(self) -> None:
        super().__init__()

        self._previous_network = psutil.net_io_counters()
        self._previous_network_time = psutil.boot_time()

        self._setup_ui()

        # Prime CPU measurement to avoid an inaccurate first reading.
        psutil.cpu_percent(interval=None)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._refresh_metrics)
        self._timer.start(1500)

        self._refresh_metrics()

    def _setup_ui(self) -> None:
        """Build the system vitals interface."""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 8, 0, 8)
        layout.setSpacing(12)

        self.metric_labels: dict[str, QLabel] = {}

        metrics = [
            ("CPU", "cpu"),
            ("MEMORY", "memory"),
            ("BATTERY", "battery"),
            ("STORAGE", "storage"),
            ("NETWORK", "network"),
            ("CPU TEMP", "temperature"),
            ("INTEL GPU", "gpu"),
        ]

        for title, key in metrics:
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                color: #718294;
                font-size: 9px;
                font-weight: 600;
                letter-spacing: 1px;
            """)

            value_label = QLabel("--")
            value_label.setStyleSheet("""
                color: #E8EEF5;
                font-size: 12px;
                font-weight: 600;
            """)

            layout.addWidget(title_label)
            layout.addWidget(value_label)

            self.metric_labels[key] = value_label

    def _refresh_metrics(self) -> None:
        """Read and display the latest system metrics."""

        # CPU
        cpu_usage = psutil.cpu_percent(interval=None)
        self.metric_labels["cpu"].setText(f"{cpu_usage:.0f}%")

        # Memory
        memory = psutil.virtual_memory()
        memory_used = memory.used / (1024 ** 3)
        memory_total = memory.total / (1024 ** 3)

        self.metric_labels["memory"].setText(
            f"{memory.percent:.0f}%  |  "
            f"{memory_used:.1f}/{memory_total:.1f} GB"
        )

        # Battery
        battery = psutil.sensors_battery()

        if battery is not None:
            self.metric_labels["battery"].setText(
                f"{battery.percent:.0f}%"
            )
        else:
            self.metric_labels["battery"].setText("N/A")

        # Storage
        drive = Path.home().anchor or "C:\\"
        disk = psutil.disk_usage(drive)

        self.metric_labels["storage"].setText(
            f"{disk.percent:.0f}% used"
        )

        # Network throughput
        current_network = psutil.net_io_counters()

        if current_network is not None and self._previous_network is not None:
            download_speed = (
                current_network.bytes_recv
                - self._previous_network.bytes_recv
            ) / 1536

            upload_speed = (
                current_network.bytes_sent
                - self._previous_network.bytes_sent
            ) / 1536

            self.metric_labels["network"].setText(
                f"↓ {download_speed:.1f} KB/s  "
                f"↑ {upload_speed:.1f} KB/s"
            )

            self._previous_network = current_network

        # Temperature (may not be exposed by Windows).
        try:
            temperatures = psutil.sensors_temperatures()
            available = [
                sensor.current
                for readings in temperatures.values()
                for sensor in readings
                if sensor.current is not None
            ]

            self.metric_labels["temperature"].setText(
                f"{max(available):.0f} °C" if available else "N/A"
            )
        except (AttributeError, OSError):
            self.metric_labels["temperature"].setText("N/A")

        # GPU monitoring will be implemented separately.
        self.metric_labels["gpu"].setText("N/A")
