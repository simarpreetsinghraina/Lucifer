
"""LUCIFER - Animated AI energy orb.

Seven states:
    idle, listening, thinking, speaking,
    executing, error, offline

Compatible with:
    orb = LuciferOrb()
    orb.set_state("thinking")
    orb.set_voice_level(0.7)
    orb.set_progress(0.65)
"""

import math
import random
import time

from PySide6.QtCore import Qt, QTimer, QSize, QRectF, QPointF
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QRadialGradient,
    QConicalGradient,
)
from PySide6.QtWidgets import QWidget


class LuciferOrb(QWidget):

    STATES = {
        "idle",
        "listening",
        "thinking",
        "speaking",
        "executing",
        "error",
        "offline",
    }

    COLORS = {
        "idle": QColor("#39BFFF"),
        "listening": QColor("#00E5FF"),
        "thinking": QColor("#657BFF"),
        "speaking": QColor("#36DFFF"),
        "executing": QColor("#FFAD42"),
        "error": QColor("#FF405D"),
        "offline": QColor("#64748B"),
    }

    def __init__(self):
        super().__init__()

        self._state = "idle"
        self._previous_color = QColor(self.COLORS["idle"])

        self._phase = 0.0
        self._rotation = 0.0
        self._voice_level = 0.0
        self._progress = 0.0

        self._transition = 1.0
        self._transition_speed = 2.5

        self._last_time = time.perf_counter()
        self._state_time = 0.0

        self._particles = []

        self._create_particles()

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumSize(220, 220)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._animate)
        self._timer.start(16)

    # --------------------------------------------------
    # PUBLIC API
    # --------------------------------------------------

    @property
    def state(self):
        return self._state

    def set_state(self, state: str):
        state = state.lower().strip()

        if state not in self.STATES:
            raise ValueError(
                f"Invalid orb state: {state}. "
                f"Available states: {sorted(self.STATES)}"
            )

        if state == self._state:
            return

        self._previous_color = QColor(self._current_color())
        self._state = state
        self._transition = 0.0
        self._state_time = 0.0

        self.update()

    def set_voice_level(self, level: float):
        """Set microphone or speech amplitude from 0.0 to 1.0."""
        self._voice_level = max(0.0, min(1.0, float(level)))

    def set_progress(self, progress: float):
        """Set execution progress from 0.0 to 1.0."""
        self._progress = max(0.0, min(1.0, float(progress)))
        self.update()

    def sizeHint(self):
        return QSize(420, 420)

    # --------------------------------------------------
    # PARTICLES
    # --------------------------------------------------

    def _create_particles(self):
        random.seed(42)

        for _ in range(42):
            self._particles.append({
                "angle": random.uniform(0, math.tau),
                "radius": random.uniform(0.29, 0.48),
                "speed": random.uniform(0.15, 0.65),
                "size": random.uniform(1.0, 3.0),
                "offset": random.uniform(0, math.tau),
                "alpha": random.randint(65, 190),
            })

        random.seed()

    # --------------------------------------------------
    # ANIMATION ENGINE
    # --------------------------------------------------

    def _animate(self):
        now = time.perf_counter()
        dt = min(now - self._last_time, 0.05)
        self._last_time = now

        self._phase += dt
        self._state_time += dt

        self._transition = min(
            1.0,
            self._transition + dt * self._transition_speed
        )

        speeds = {
            "idle": 0.20,
            "listening": 0.75,
            "thinking": 1.25,
            "speaking": 0.90,
            "executing": 1.65,
            "error": 0.55,
            "offline": 0.04,
        }

        self._rotation += dt * speeds[self._state]

        # Voice input naturally settles when there is no new input.
        self._voice_level *= max(0.0, 1.0 - dt * 3.5)

        self.update()

    # --------------------------------------------------
    # COLOR MANAGEMENT
    # --------------------------------------------------

    def _current_color(self):
        return QColor(self.COLORS[self._state])

    def _get_color(self):
        target = self._current_color()
        start = self._previous_color

        t = self._transition
        t = t * t * (3.0 - 2.0 * t)

        return QColor(
            int(start.red() + (target.red() - start.red()) * t),
            int(start.green() + (target.green() - start.green()) * t),
            int(start.blue() + (target.blue() - start.blue()) * t),
        )

    @staticmethod
    def _with_alpha(color, alpha):
        result = QColor(color)
        result.setAlpha(max(0, min(255, int(alpha))))
        return result

    # --------------------------------------------------
    # MAIN PAINT EVENT
    # --------------------------------------------------

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        width = self.width()
        height = self.height()

        center = QPointF(width / 2, height / 2)
        unit = min(width, height)

        color = self._get_color()

        # Keep the orb centered and responsive to widget size.
        painter.translate(center)

        self._draw_outer_glow(painter, unit, color)
        self._draw_particles(painter, unit, color)
        self._draw_orbital_rings(painter, unit, color)
        self._draw_energy_core(painter, unit, color)

        painter.end()

    # --------------------------------------------------
    # OUTER GLOW
    # --------------------------------------------------

    def _draw_outer_glow(self, painter, unit, color):

        pulse = math.sin(self._phase * 1.5) * 0.035

        if self._state == "idle":
            intensity = 0.55 + pulse

        elif self._state == "listening":
            intensity = 0.65 + self._voice_level * 0.35

        elif self._state == "thinking":
            intensity = 0.65 + abs(math.sin(self._phase * 2.0)) * 0.25

        elif self._state == "speaking":
            intensity = 0.65 + self._voice_level * 0.35

        elif self._state == "executing":
            intensity = 0.7 + abs(math.sin(self._phase * 3.0)) * 0.2

        elif self._state == "error":
            intensity = 0.45 + abs(math.sin(self._phase * 8.0)) * 0.35

        else:
            intensity = 0.18

        radius = unit * (0.40 + pulse)

        gradient = QRadialGradient(
            QPointF(0, 0),
            radius * 1.45,
        )

        gradient.setColorAt(
            0.0,
            self._with_alpha(color, 0)
        )

        gradient.setColorAt(
            0.40,
            self._with_alpha(color, int(40 * intensity))
        )

        gradient.setColorAt(
            0.72,
            self._with_alpha(color, int(20 * intensity))
        )

        gradient.setColorAt(1.0, QColor(0, 0, 0, 0))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(gradient)

        painter.drawEllipse(
            QRectF(-radius * 1.45, -radius * 1.45,
                   radius * 2.9, radius * 2.9)
        )

    # --------------------------------------------------
    # PARTICLE SYSTEM
    # --------------------------------------------------

    def _draw_particles(self, painter, unit, color):

        if self._state == "offline":
            return

        if self._state == "error":
            movement = 0.25
        elif self._state == "executing":
            movement = 1.8
        elif self._state == "thinking":
            movement = 1.35
        elif self._state == "listening":
            movement = 0.75
        else:
            movement = 0.45

        painter.setPen(Qt.PenStyle.NoPen)

        for particle in self._particles:

            angle = (
                particle["angle"]
                + self._rotation * particle["speed"] * movement
                + math.sin(
                    self._phase + particle["offset"]
                ) * 0.08
            )

            radius = unit * particle["radius"]

            if self._state == "listening":
                radius += self._voice_level * 12

            if self._state == "speaking":
                radius += self._voice_level * 15

            x = math.cos(angle) * radius
            y = math.sin(angle) * radius

            alpha = particle["alpha"]

            if self._state == "thinking":
                alpha = int(alpha * (
                    0.5 + 0.5 * abs(math.sin(
                        self._phase * 2 + particle["offset"]
                    ))
                ))

            elif self._state == "executing":
                alpha = int(alpha * (
                    0.55 + 0.45 * abs(math.sin(
                        self._phase * 4 + particle["offset"]
                    ))
                ))

            elif self._state == "error":
                alpha = int(alpha * (
                    0.35 + 0.65 * abs(math.sin(
                        self._phase * 9 + particle["offset"]
                    ))
                ))

            particle_color = self._with_alpha(color, alpha)

            painter.setBrush(particle_color)

            size = particle["size"]

            painter.drawEllipse(
                QPointF(x, y),
                size,
                size
            )

    # --------------------------------------------------
    # ORBITAL RINGS
    # --------------------------------------------------

    def _draw_orbital_rings(self, painter, unit, color):

        base = unit * 0.335

        if self._state == "offline":
            alpha = 30
        else:
            alpha = 105

        if self._state == "thinking":
            rotation_speed = 2.4
        elif self._state == "executing":
            rotation_speed = 3.2
        elif self._state == "listening":
            rotation_speed = 1.5
        elif self._state == "error":
            rotation_speed = 0.8
        else:
            rotation_speed = 0.5

        painter.save()

        # Main orbital ring.
        painter.rotate(math.degrees(self._rotation * rotation_speed))

        pen = QPen(
            self._with_alpha(color, alpha),
            1.5
        )

        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        painter.drawEllipse(
            QRectF(-base, -base * 0.42, base * 2, base * 0.84)
        )

        # Secondary tilted orbit.
        painter.rotate(65)

        painter.setPen(
            QPen(
                self._with_alpha(color, alpha // 2),
                1.0
            )
        )

        painter.drawEllipse(
            QRectF(-base * 1.08, -base * 0.30,
                   base * 2.16, base * 0.60)
        )

        painter.restore()

        # Rotating energy arcs.
        self._draw_energy_arcs(painter, unit, color)

        # Executing progress indicator.
        if self._state == "executing":
            self._draw_progress(painter, unit, color)

    # --------------------------------------------------
    # ENERGY ARCS
    # --------------------------------------------------

    def _draw_energy_arcs(self, painter, unit, color):

        radius = unit * 0.365

        if self._state == "offline":
            return

        if self._state == "thinking":
            arc_count = 4
            speed = 2.8
        elif self._state == "executing":
            arc_count = 5
            speed = 3.8
        elif self._state == "listening":
            arc_count = 3
            speed = 1.8
        elif self._state == "speaking":
            arc_count = 4
            speed = 2.2
        else:
            arc_count = 3
            speed = 0.8

        for i in range(arc_count):

            start_angle = int(
                (self._rotation * speed * 57.2958 + i * 120) * 16
            )

            span = int((35 + i * 8) * 16)

            pen = QPen(
                self._with_alpha(color, 150 - i * 20),
                2.0 if i == 0 else 1.2
            )

            pen.setCapStyle(Qt.PenCapStyle.RoundCap)

            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)

            painter.drawArc(
                QRectF(-radius, -radius, radius * 2, radius * 2),
                start_angle,
                span
            )

    # --------------------------------------------------
    # EXECUTION PROGRESS
    # --------------------------------------------------

    def _draw_progress(self, painter, unit, color):

        radius = unit * 0.405

        painter.setBrush(Qt.BrushStyle.NoBrush)

        painter.setPen(
            QPen(
                self._with_alpha(color, 35),
                3
            )
        )

        painter.drawEllipse(
            QRectF(-radius, -radius, radius * 2, radius * 2)
        )

        pen = QPen(color, 3)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        painter.setPen(pen)

        painter.drawArc(
            QRectF(-radius, -radius, radius * 2, radius * 2),
            90 * 16,
            -int(self._progress * 360 * 16)
        )

    # --------------------------------------------------
    # CENTRAL ENERGY CORE
    # --------------------------------------------------

    def _draw_energy_core(self, painter, unit, color):

        # Different breathing patterns per state.
        if self._state == "idle":
            pulse = math.sin(self._phase * 1.5) * 0.025
            radius = unit * (0.235 + pulse)

        elif self._state == "listening":
            pulse = self._voice_level * 0.035
            radius = unit * (0.235 + pulse)

        elif self._state == "thinking":
            pulse = math.sin(self._phase * 3.0) * 0.025
            radius = unit * (0.235 + pulse)

        elif self._state == "speaking":
            pulse = self._voice_level * 0.04
            radius = unit * (0.235 + pulse)

        elif self._state == "executing":
            pulse = math.sin(self._phase * 5.0) * 0.018
            radius = unit * (0.235 + pulse)

        elif self._state == "error":
            pulse = math.sin(self._phase * 10.0) * 0.025
            radius = unit * (0.235 + pulse)

        else:
            radius = unit * 0.22

        # Error glitch displacement.
        offset_x = 0.0
        offset_y = 0.0

        if self._state == "error":
            glitch = math.sin(self._phase * 18)

            if glitch > 0.85:
                offset_x = math.sin(self._phase * 55) * 4
                offset_y = math.cos(self._phase * 45) * 2

        painter.save()
        painter.translate(offset_x, offset_y)

        # Soft outer illumination.
        glow = QRadialGradient(
            QPointF(0, 0),
            radius * 1.7
        )

        glow.setColorAt(
            0.0,
            self._with_alpha(color, 95)
        )

        glow.setColorAt(
            0.45,
            self._with_alpha(color, 45)
        )

        glow.setColorAt(
            1.0,
            QColor(0, 0, 0, 0)
        )

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(glow)

        painter.drawEllipse(
            QRectF(-radius * 1.7, -radius * 1.7,
                   radius * 3.4, radius * 3.4)
        )

        # Solid spherical core with radial illumination.
        core = QRadialGradient(
            QPointF(-radius * 0.28, -radius * 0.30),
            radius * 1.55
        )

        core.setColorAt(0.0, QColor("#FFFFFF"))
        core.setColorAt(0.12, self._with_alpha(color, 255))
        core.setColorAt(0.48, self._with_alpha(color, 245))
        core.setColorAt(0.78, self._with_alpha(color.darker(150), 255))
        core.setColorAt(1.0, QColor("#07101D"))

        painter.setBrush(core)
        painter.setPen(
            QPen(
                self._with_alpha(color, 180),
                1.5
            )
        )

        painter.drawEllipse(
            QRectF(-radius, -radius, radius * 2, radius * 2)
        )

        # Internal plasma movement.
        self._draw_internal_plasma(
            painter,
            radius,
            color
        )

        # Small central highlight.
        highlight = QRadialGradient(
            QPointF(-radius * 0.28, -radius * 0.30),
            radius * 0.42
        )

        highlight.setColorAt(0.0, QColor(255, 255, 255, 150))
        highlight.setColorAt(1.0, QColor(255, 255, 255, 0))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(highlight)

        painter.drawEllipse(
            QRectF(
                -radius * 0.65,
                -radius * 0.65,
                radius * 1.3,
                radius * 1.3
            )
        )

        painter.restore()

    # --------------------------------------------------
    # INTERNAL PLASMA
    # --------------------------------------------------

    def _draw_internal_plasma(self, painter, radius, color):

        painter.save()

        # Keep plasma contained inside the spherical core.
        painter.setClipRect(
            QRectF(
                -radius,
                -radius,
                radius * 2,
                radius * 2
            )
        )

        painter.setPen(Qt.PenStyle.NoPen)

        for i in range(7):

            angle = (
                self._phase * (0.7 + i * 0.13)
                + i * 1.7
            )

            orbit = radius * (0.15 + i * 0.085)

            x = math.cos(angle) * orbit
            y = math.sin(angle * 1.4) * orbit

            blob_size = radius * (0.12 + 0.025 * math.sin(
                self._phase * 2 + i
            ))

            plasma = QRadialGradient(
                QPointF(x, y),
                blob_size * 2
            )

            plasma.setColorAt(
                0.0,
                QColor(255, 255, 255, 110)
            )

            plasma.setColorAt(
                0.3,
                self._with_alpha(color.lighter(160), 90)
            )

            plasma.setColorAt(
                1.0,
                QColor(0, 0, 0, 0)
            )

            painter.setBrush(plasma)

            painter.drawEllipse(
                QPointF(x, y),
                blob_size * 2,
                blob_size * 2
            )

        painter.restore()
