"""Implements rendering-related classes that subclass `System`."""
import glfw
import OpenGL.GL as gl

from engine.entity import Entity
from engine.system import System, PipelinedSystem
from engine.transform import Transform

from .camera import Camera
from .lighting import Lamp
from .mesh import Mesh
from .sprite import Sprite
from .text import Text
from .renderers import MeshRenderer, SpriteRenderer, TextRenderer


class RenderingSystem(PipelinedSystem):
    """System that renders objects in a scene."""

    def __init__(self):
        """Construct and pipeline the systems needed to render a scene."""
        super().__init__([
            WindowClearSystem(),
            TextRenderingSystem(),
            SpriteRenderingSystem(),
            MeshRenderingSystem(),
            BufferSwapSystem()
        ])


class WindowClearSystem(System):
    """System that clears the pixels on the screen."""

    def step(self, delta: float) -> None:
        """Clear the pixels on the screen."""
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)


class TextRenderingSystem(System):
    """System that renders text."""

    REQUIRED_COMPONENTS = Transform, Text

    def start(self) -> None:
        self.camera = None
        self.renderer = None

    def step(self, delta: float) -> None:
        """Render text in the scene."""
        for entity in self.entities:
            self.renderer.draw(entity[Text], entity[Transform])

    def add(self, entity: Entity) -> None:
        if isinstance(entity, Camera) and not self.camera:
            self.camera = entity
            self.renderer = TextRenderer(entity)
            return

        if isinstance(entity, Camera) and self.camera:
            raise AttributeError("Camera is already set")

        super().add(entity)

    def remove(self, entity: Entity) -> None:
        if entity is self.camera:
            self.camera = None
            self.renderer = None
            return

        super().remove(entity)


class SpriteRenderingSystem(System):
    """System that renders sprite."""

    REQUIRED_COMPONENTS = Transform, Sprite

    def start(self) -> None:
        """Construct a sprite renderer."""
        self.camera = None
        self.renderer = None

    def step(self, delta: float) -> None:
        """Render each sprite in the scene."""
        for entity in self.entities:
            self.renderer.draw(entity[Sprite], entity[Transform])

    def add(self, entity: Entity) -> None:
        if isinstance(entity, Camera) and not self.camera:
            self.camera = entity
            self.renderer = SpriteRenderer(entity)
            return

        if isinstance(entity, Camera) and self.camera:
            raise AttributeError("Camera is already set")

        super().add(entity)

    def remove(self, entity: Entity) -> None:
        if entity is self.camera:
            self.camera = None
            self.renderer = None
            return

        super().remove(entity)


class MeshRenderingSystem(System):
    """System that renders a mesh."""

    def start(self) -> None:
        """Construct a Mesh renderer."""
        self.camera = None
        self.renderer = None

    def step(self, delta: float) -> None:
        """Render each mesh in the scene."""
        for entity in self.entities:
            self.renderer.draw(entity[Mesh], entity[Transform])

    def add(self, entity: Entity) -> None:
        if isinstance(entity, Camera) and not self.camera:
            self.camera = entity
            self.renderer = MeshRenderer(entity)
            return

        if isinstance(entity, Camera) and self.camera:
            raise AttributeError("Camera is already set")

        super().add(entity)

    def remove(self, entity: Entity) -> None:
        if entity is self.camera:
            self.camera = None
            self.renderer = None
            return

        super().remove(entity)


class BufferSwapSystem(System):
    """System that swaps buffers."""

    def start(self) -> None:
        """Get a reference to the window."""
        self.window = glfw.get_current_context()

    def step(self, delta: float) -> None:
        """Swap buffers."""
        glfw.swap_buffers(self.window)
