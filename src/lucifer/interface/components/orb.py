
"""Animated energy core for LUCIFER."""

import math
import random
import time

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPainterPath,
    QPen,
    QRadialGradient,
)
from PySide6.QtWidgets import QWidget


class LuciferOrb(QWidget):
    """A layered, animated energy core with smooth state transitions."""

    STATES = (
        "idle",
        "listening",
        "thinking",
        "speaking",
        "executing",
        "error",
        "offline",
    )

    PALETTES = {
        "idle": ("#72D5E8", "#168DB5", "#071B2B"),
        "listening": ("#8CEBFF", "#22B9E8", "#092B43"),
        "thinking": ("#75C8FF", "#287CE0", "#101D42"),
        "speaking": ("#A0F1FF", "#31A9D5", "#0A2940"),
        "executing": ("#B0EFFF", "#278FD0", "#102C4A"),
        "error": ("#FF8888", "#C83D55", "#3B101C"),
        "offline": ("#637887", "#344B5A", "#111A22"),
    }

    # Animation characteristics for each state.
    # Values are smoothly interpolated during transitions.
    PROFILES = {
        "idle": {
            "pulse_speed": 1.0,
            "pulse_amount": 0.045,
            "orbit_speed": 0.55,
            "plasma_speed": 0.85,
            "particle_speed": 1.0,
            "atmosphere_alpha": 55,
            "orbit_alpha": 1.0,
            "plasma_alpha": 1.0,
            "particle_alpha": 185,
            "waves": 0.0,
        },
        "listening": {
            "pulse_speed": 2.8,
            "pulse_amount": 0.075,
            "orbit_speed": 1.0,
            "plasma_speed": 1.5,
            "particle_speed": 1.4,
            "atmosphere_alpha": 85,
            "orbit_alpha": 1.2,
            "plasma_alpha": 1.2,
            "particle_alpha": 220,
            "waves": 1.0,
        },
        "thinking": {
            "pulse_speed": 1.8,
            "pulse_amount": 0.055,
            "orbit_speed": 1.6,
            "plasma_speed": 2.0,
            "particle_speed": 2.0,
            "atmosphere_alpha": 65,
            "orbit_alpha": 1.2,
            "plasma_alpha": 1.1,
            "particle_alpha": 200,
            "waves": 0.0,
        },
        "speaking": {
            "pulse_speed": 3.5,
            "pulse_amount": 0.09,
            "orbit_speed": 1.1,
            "plasma_speed": 2.5,
            "particle_speed": 1.5,
            "atmosphere_alpha": 90,
            "orbit_alpha": 1.1,
            "plasma_alpha": 1.3,
            "particle_alpha": 225,
            "waves": 0.0,
        },
        "executing": {
            "pulse_speed": 2.4,
            "pulse_amount": 0.07,
            "orbit_speed": 2.2,
            "plasma_speed": 2.8,
            "particle_speed": 2.2,
            "atmosphere_alpha": 80,
            "orbit_alpha": 1.4,
            "plasma_alpha": 1.3,
            "particle_alpha": 220,
            "waves": 0.0,
        },
        "error": {
            "pulse_speed": 4.0,
            "pulse_amount": 0.10,
            "orbit_speed": 2.8,
            "plasma_speed": 3.0,
            "particle_speed": 1.6,
            "atmosphere_alpha": 95,
            "orbit_alpha": 1.3,
            "plasma_alpha": 1.2,
            "particle_alpha": 230,
            "waves": 0.0,
        },
        "offline": {
            "pulse_speed": 0.0,
            "pulse_amount": 0.0,
            "orbit_speed": 0.0,
            "plasma_speed": 0.0,
            "particle_speed": 0.0,
            "atmosphere_alpha": 12,
            "orbit_alpha": 0.0,
            "plasma_alpha": 0.0,
            "particle_alpha": 0,
            "waves": 0.0,
        },
    }

    def __init__(self, parent=None):
        super().__init__(parent)

        self._state = "idle"
        self._previous_state = "idle"

        self._start_time = time.monotonic()
        self._transition_start = self._start_time
        self._transition_duration = 0.6

        self._transition_from_palette = [
            QColor(c) for c in self.PALETTES["idle"]
        ]

        self._transition_from_visual = dict(
            self.PROFILES["idle"]
        )

        self._particles = []
        rng = random.Random(42)

        for _ in range(48):
            self._particles.append({
                "angle": rng.uniform(0, math.tau),
                "radius": rng.uniform(0.66, 1.02),
                "speed": rng.uniform(0.12, 0.48),
                "size": rng.uniform(1.0, 2.8),
                "phase": rng.uniform(0, math.tau),
            })

        self.setMinimumSize(250, 250)

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update)
        self._timer.start(33)

    # ---------------------------------------------------------
    # State management
    # ---------------------------------------------------------

    def set_state(self, state: str) -> None:
        """Change the orb's operational state smoothly."""

        state = state.lower().strip()

        if state not in self.STATES:
            raise ValueError(f"Unknown orb state: {state}")

        if state == self._state:
            return

        self._previous_state = self._state
        self._state = state
        self._transition_start = time.monotonic()

        self.update()

    def get_state(self) -> str:
        """Return the current operational state."""

        return self._state

    def _get_transition_progress(self) -> float:
        """Calculate smooth transition progress."""

        elapsed = time.monotonic() - self._transition_start

        progress = min(
            elapsed / self._transition_duration,
            1.0,
        )

        # Smoothstep easing.
        return progress * progress * (3.0 - 2.0 * progress)

    @staticmethod
    def _blend_value(start: float, end: float, amount: float) -> float:
        """Interpolate between two numeric values."""

        return start + (end - start) * amount

    @staticmethod
    def _blend_color(
        start: QColor,
        end: QColor,
        amount: float,
    ) -> QColor:
        """Interpolate smoothly between two colours."""

        amount = max(0.0, min(amount, 1.0))

        return QColor(
            round(start.red() + (end.red() - start.red()) * amount),
            round(start.green() + (end.green() - start.green()) * amount),
            round(start.blue() + (end.blue() - start.blue()) * amount),
            round(start.alpha() + (end.alpha() - start.alpha()) * amount),
        )

    def _get_visual_properties(self, progress: float) -> dict:
        """Blend the animation properties of both states."""

        old = self.PROFILES[self._previous_state]
        new = self.PROFILES[self._state]

        return {
            key: self._blend_value(old[key], new[key], progress)
            for key in old
        }

    # ---------------------------------------------------------
    # Main rendering
    # ---------------------------------------------------------

    def paintEvent(self, event):
        """Render the animated energy core."""

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        size = min(self.width(), self.height())

        center = QPointF(
            self.width() / 2,
            self.height() / 2,
        )

        radius = size * 0.31
        t = time.monotonic() - self._start_time

        progress = self._get_transition_progress()
        visual = self._get_visual_properties(progress)

        old_palette = self.PALETTES[self._previous_state]
        new_palette = self.PALETTES[self._state]

        primary = self._blend_color(
            QColor(old_palette[0]),
            QColor(new_palette[0]),
            progress,
        )

        secondary = self._blend_color(
            QColor(old_palette[1]),
            QColor(new_palette[1]),
            progress,
        )

        dark = self._blend_color(
            QColor(old_palette[2]),
            QColor(new_palette[2]),
            progress,
        )

        pulse_speed = visual["pulse_speed"]
        pulse_amount = visual["pulse_amount"]

        pulse = (
            1.0
            + pulse_amount * math.sin(t * pulse_speed)
        )

        # Atmospheric glow.
        self._draw_atmosphere(
            painter,
            center,
            radius,
            primary,
            visual["atmosphere_alpha"],
            pulse,
        )

        # Listening waves fade in and out.
        if visual["waves"] > 0.001:
            self._draw_listening_waves(
                painter,
                center,
                radius,
                primary,
                t,
                visual["waves"],
            )

        # Orbital structures.
        if visual["orbit_alpha"] > 0.001:
            self._draw_orbits(
                painter,
                center,
                radius,
                primary,
                secondary,
                t,
                visual["orbit_speed"],
                visual["orbit_alpha"],
            )

        # Main energy sphere.
        self._draw_core(
            painter,
            center,
            radius,
            primary,
            secondary,
            dark,
            pulse,
        )

        # Internal plasma currents.
        if visual["plasma_alpha"] > 0.001:
            self._draw_plasma(
                painter,
                center,
                radius,
                primary,
                secondary,
                t,
                visual["plasma_speed"],
                visual["plasma_alpha"],
            )

        # Orbiting particles.
        if visual["particle_alpha"] > 0:
            self._draw_particles(
                painter,
                center,
                radius,
                primary,
                t,
                visual["particle_speed"],
                visual["particle_alpha"],
            )

        painter.end()

    # ---------------------------------------------------------
    # Atmosphere
    # ---------------------------------------------------------

    def _draw_atmosphere(
        self,
        painter,
        center,
        radius,
        color,
        alpha,
        pulse,
    ):
        """Draw the soft light surrounding the core."""

        glow_radius = radius * 1.75 * pulse

        gradient = QRadialGradient(
            center,
            glow_radius,
        )

        inner = QColor(color)
        inner.setAlpha(max(0, min(255, round(alpha))))

        middle = QColor(color)
        middle.setAlpha(max(0, min(255, round(alpha * 0.36))))

        gradient.setColorAt(0.0, inner)
        gradient.setColorAt(0.48, middle)
        gradient.setColorAt(1.0, QColor(0, 0, 0, 0))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(gradient)

        painter.drawEllipse(
            center,
            glow_radius,
            glow_radius,
        )

    # ---------------------------------------------------------
    # Listening waves
    # ---------------------------------------------------------

    def _draw_listening_waves(
        self,
        painter,
        center,
        radius,
        color,
        t,
        intensity,
    ):
        """Draw expanding sound-wave rings."""

        painter.save()
        painter.setBrush(Qt.BrushStyle.NoBrush)

        for i in range(3):
            phase = (t * 0.65 + i / 3) % 1.0

            wave_radius = radius * (
                1.22 + phase * 0.65
            )

            alpha = int(
                115 * (1.0 - phase) * intensity
            )

            wave_color = QColor(color)
            wave_color.setAlpha(
                max(0, min(255, alpha))
            )

            pen = QPen(wave_color)
            pen.setWidthF(1.5)

            painter.setPen(pen)

            painter.drawEllipse(
                center,
                wave_radius,
                wave_radius,
            )

        painter.restore()

    # ---------------------------------------------------------
    # Orbital structures
    # ---------------------------------------------------------

    def _draw_orbits(
        self,
        painter,
        center,
        radius,
        primary,
        secondary,
        t,
        orbit_speed,
        intensity,
    ):
        """Draw rotating orbital energy structures."""

        painter.save()
        painter.setBrush(Qt.BrushStyle.NoBrush)

        orbit_configs = [
            (1.48, 0.58, 25, 0.32),
            (1.58, 0.48, -48, -0.24),
            (1.34, 0.72, 82, 0.18),
        ]

        for index, (rx, ry, tilt, direction) in enumerate(
            orbit_configs
        ):
            painter.save()
            painter.translate(center)

            painter.rotate(
                tilt + t * direction * orbit_speed
            )

            orbit_color = QColor(
                primary if index != 1 else secondary
            )

            base_alpha = 105 if index == 0 else 65

            orbit_color.setAlpha(
                max(0, min(255, round(base_alpha * intensity)))
            )

            pen = QPen(orbit_color)
            pen.setWidthF(
                1.15 if index == 0 else 0.8
            )

            painter.setPen(pen)

            painter.drawEllipse(
                QRectF(
                    -radius * rx,
                    -radius * ry,
                    radius * rx * 2,
                    radius * ry * 2,
                )
            )

            # Luminous orbital marker.
            marker_angle = (
                t * direction * orbit_speed
                + index * 2.1
            )

            marker_x = math.cos(marker_angle) * radius * rx
            marker_y = math.sin(marker_angle) * radius * ry

            marker_color = QColor(primary)
            marker_color.setAlpha(
                max(0, min(255, round(210 * intensity)))
            )

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(marker_color)

            painter.drawEllipse(
                QPointF(marker_x, marker_y),
                3.0,
                3.0,
            )

            painter.restore()

        painter.restore()

    # ---------------------------------------------------------
    # Main energy core
    # ---------------------------------------------------------

    def _draw_core(
        self,
        painter,
        center,
        radius,
        primary,
        secondary,
        dark,
        pulse,
    ):
        """Draw the main spherical energy body."""

        core_radius = radius * pulse

        gradient = QRadialGradient(
            QPointF(
                center.x() - radius * 0.30,
                center.y() - radius * 0.35,
            ),
            core_radius * 1.75,
        )

        highlight = QColor(primary)
        highlight.setAlpha(240)

        mid = QColor(secondary)
        mid.setAlpha(235)

        deep = QColor(dark)
        deep.setAlpha(255)

        gradient.setColorAt(0.0, highlight)
        gradient.setColorAt(0.25, mid)
        gradient.setColorAt(0.72, deep)
        gradient.setColorAt(1.0, QColor(3, 9, 17, 255))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(gradient)

        painter.drawEllipse(
            center,
            core_radius,
            core_radius,
        )

        # Illuminated outer edge.
        edge = QColor(primary)
        edge.setAlpha(155)

        pen = QPen(edge)
        pen.setWidthF(1.5)

        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        painter.drawEllipse(
            center,
            core_radius,
            core_radius,
        )

    # ---------------------------------------------------------
    # Internal plasma
    # ---------------------------------------------------------

    def _draw_plasma(
        self,
        painter,
        center,
        radius,
        primary,
        secondary,
        t,
        speed,
        intensity,
    ):
        """Draw flowing plasma currents inside the sphere."""

        painter.save()

        clip_path = QPainterPath()

        clip_path.addEllipse(
            center,
            radius * 0.96,
            radius * 0.96,
        )

        painter.setClipPath(clip_path)

        for i in range(7):
            phase = t * speed + i * 0.83

            path = QPainterPath()

            start_x = center.x() - radius * 1.15

            start_y = (
                center.y()
                + math.sin(phase) * radius * 0.55
            )

            path.moveTo(start_x, start_y)

            path.cubicTo(
                center.x() - radius * 0.5,
                center.y() - math.cos(phase * 1.1) * radius,
                center.x() + radius * 0.4,
                center.y() + math.sin(phase * 0.8) * radius,
                center.x() + radius * 1.15,
                center.y() + math.cos(phase) * radius * 0.55,
            )

            plasma_color = QColor(
                primary if i % 2 == 0 else secondary
            )

            base_alpha = 115 if i % 2 == 0 else 75

            plasma_color.setAlpha(
                max(0, min(255, round(base_alpha * intensity)))
            )

            pen = QPen(plasma_color)

            pen.setWidthF(
                1.4 if i % 2 == 0 else 0.9
            )

            pen.setCapStyle(
                Qt.PenCapStyle.RoundCap
            )

            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)

            painter.drawPath(path)

        # Central energy glow.
        center_glow = QRadialGradient(
            QPointF(
                center.x() - radius * 0.05,
                center.y() - radius * 0.05,
            ),
            radius * 0.62,
        )

        glow_color = QColor(primary)
        glow_color.setAlpha(
            max(0, min(255, round(75 * intensity)))
        )

        center_glow.setColorAt(0.0, glow_color)
        center_glow.setColorAt(
            1.0,
            QColor(0, 0, 0, 0),
        )

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(center_glow)

        painter.drawEllipse(
            center,
            radius * 0.62,
            radius * 0.62,
        )

        painter.restore()

    # ---------------------------------------------------------
    # Orbiting particles
    # ---------------------------------------------------------

    def _draw_particles(
        self,
        painter,
        center,
        radius,
        color,
        t,
        speed,
        intensity,
    ):
        """Draw particles orbiting around the energy core."""

        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)

        for particle in self._particles:
            angle = (
                particle["angle"]
                + t * particle["speed"] * speed
            )

            radius_factor = particle["radius"]

            if self._state == "executing":
                radius_factor += (
                    0.04
                    * math.sin(
                        t * 2.0 + particle["phase"]
                    )
                    * intensity
                )

            x = (
                center.x()
                + math.cos(angle) * radius * radius_factor
            )

            y = (
                center.y()
                + math.sin(angle) * radius * radius_factor
            )

            flicker = (
                0.55
                + 0.45 * math.sin(
                    t * 2.0 + particle["phase"]
                )
            )

            particle_color = QColor(color)

            particle_color.setAlpha(
                max(0, min(255, round(intensity * flicker)))
            )

            painter.setBrush(particle_color)

            particle_size = particle["size"]

            painter.drawEllipse(
                QPointF(x, y),
                particle_size,
                particle_size,
            )

        painter.restore()
