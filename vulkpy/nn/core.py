from __future__ import annotations
from typing import Callable, Iterable, Optional

from vulkpy.vkarray import GPU, Array
from .optimizers import Optimizer, Adam


__all__ = [
    "Parameter",
    "Module",
    "Loss"
]


class Parameter:
    """
    Neural Network Parameter
    """
    def __init__(self,
                 gpu: GPU,
                 shape: Iterable[int],
                 trainable: bool = True,
                 opt: Optional[Optimizer] = None,
                 initializer: Optional[Callable[[GPU, Iterable[int]], Array]]=None):
        """
        Initialize Parameter

        Parameters
        ----------
        gpu : vulkpy.GPU
            GPU
        shape : iterable of ints
            Shape of parameter
        trainable : bool, optional
            If ``True`` (default), track gradient
        opt : vulkpy.nn.Optimizer, optional
            Optimizer. If ``None`` (default), ``vulkpy.nn.Adam`` is used.
        initializer : callable, optional
            Initializer function. If ``None`` (default), initialized with ``0.0``.
        """
        if initializer is None:
            self.value = Array(gpu, shape=shape)
            self.value[:] = 0.0
        else:
            self.value = initializer(gpu, shape=shape)

        if trainable:
            self.grad = Array(gpu, shape=shape)
            self.grad[:] = 0.0

            if opt is None:
                opt = Adam(gpu)
            self.opt = opt
            self.opt_state = self.opt.init_state(shape)
        else:
            self.grad = None

    def is_trainable(self) -> bool:
        """
        Whether this parameter is trainable

        Returns
        -------
        bool
            Is trainable
        """
        return self.grad is not None

    def add_grad(self, grad: Array):
        """
        Add gradient

        Parameters
        ----------
        grad : vulkpy.Array
            Gradient to be accumulated
        """
        self.grad += grad

    def zero_grad(self):
        """
        Clear gradient to 0.0
        """
        self.grad[:] = 0.0

    def update(self):
        """
        Update value

        Update value with accumulated gradients only if this value is trainable.
        """
        if self.is_trainable():
            self.value += self.opt(self.grad, self.opt_state)

class Module:
    def __init__(self):
        pass

    def __call__(self, x: Array) -> Array:
        """
        Call Module

        Parameters
        ----------
        x : vulkpy.Array
            Input

        Returns
        -------
        y : vulkpy.Array
            Output

        Raises
        ------
        ValueError
            If input (``x``) shape doesn't have at least 2-dimensions.

        Notes
        -----
        This function stores input (``x``) and output (``y``) for training.
        """
        if len(x.shape) < 2:
            raise ValueError("Input must have at least 2-dimensions.")

        self._x = x
        self._y = self.forward(x)
        return self._y

    def forward(self, x: Array) -> Array:
        raise NotImplementedError

    def backward(self, dy: Array) -> Array:
        raise NotImplementedError

    def zero_grad(self):
        pass

    def update(self):
        pass

class Loss:
    def __init__(self, reduce: Literal["mean", "sum"] = "mean"):
        self.reduce, self.scale_backward = {
            "mean": (lambda _L: _L.mean(axis=0), lambda _dx: 1/_dx.shape[0]),
            "sum": (lambda _L: _L.sum(axis=0), None),
        }[reduce]

    def __call__(self, x: Array, y: Array) -> Array:
        r"""
        Compute Loss

        Parameters
        ----------
        x : vulkpy.Array
            Batch input features
        y : vulkpy.Array
            Batch labels/targets

        Returns
        -------
        loss : vulkpy.Array
            Loss
        """
        self._x = x
        self._y = y
        L = self.forward(x, y)
        return self.reduce(L)

    def grad(self) -> Array:
        r"""
        Compute Gradients

        Returns
        -------
        dx : vulkpy.Array
            Batch gradients of dL/dx

        Notes
        -----
        This method calculates gradients for the last ``__call__(x, y)``.
        """
        dx = self.backward()
        if self.scale_backward is not None:
            dx *= self.scale_backward(dx)
        return dx

    def forward(self, x: Array, y: Array) -> Array:
        raise NotImplementedError

    def backward(self) -> Array:
        raise NotImplementedError
