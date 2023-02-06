from __future__ import annotations

import os
import functools
from typing import Iterable, Optional, Self, Union

import numpy as np

from . import _vkarray

shader_dir = os.path.join(os.path.dirname(__file__), "shader")

Params = Union[_vkarray.VectorParams,
               _vkarray.VectorScalarParams,
               _vkarray.VectorScalar2Params,
               _vkarray.MatMulParams]
Op = Union[_vkarray.OpVec1, _vkarray.OpVec2, _vkarray.OpVec3, _vkarray.OpVec4,
           _vkarray.OpVecScalar1, _vkarray.OpVecScalar2, _vkarray.OpVecScalar3,
           _vkarray.OpVec2Scalar1, _vkarray.OpVec2Scalar2,
           _vkarray.OpMatMul]

class GPU:
    def __init__(self, idx: int=0, priority: float=0.0):
        """
        GPU

        Parameters
        ----------
        idx : int, optional
            Index to specify one GPU from multiple GPUs. Default is ``0``.
        priority : float, optional
            GPU priority. Default is ``0.0``.
        """
        self.gpu = _vkarray.createGPU(idx, priority)

    @functools.cache
    def _createOp(self, spv: str,
                  n: int,
                  params: Params,
                  local_size_x: int,
                  local_size_y: int,
                  local_size_z: int) -> Op:
        """
        Create GPU Operation

        Parameters
        ----------
        spv : str
            Compute Shader file name of SPIR-V (.spv)
        n : int
            Number of buffers
        params : Params
            Parameters
        local_size_x, local_size_y, local_size_z : int
            Subgroup size of compute shader

        Returns
        -------
        std::shared_ptr<Op>
           Operation
        """
        return self.gpu.createOp(n, params,
                                 spv, local_size_x, local_size_y, local_size_z)

    def _submit(self,
                spv: str,
                local_size_x: int, local_size_y: int, local_size_z: int,
                buffers: Iterable[_vkarray.Buffer],
                shape: _vkarray.DataShape,
                params: Params,
                semaphores: Iterable[_vkarray.Semaphore]) -> _vkarray.Job:
        """
        Submit GPU Operation

        Parameters
        ----------
        spv : str
            Compute Shader file name of SPIR-V (.spv)
        local_size_x, local_size_y, local_size_z : int
            Subgroup size of compute shader
        buffers : iterable of _vkarray.Buffer
            Buffers to be submitted.
        shape : _vkarray.DataShape
            Shape of data
        params : _vkarray.VectorParams, _vkarrayVectorScalarParams
            Parameters
        semaphores : iterable of _vkarray.Semaphore
            Depending Semaphores to be waited.

        Returns
        -------
        std::shared_ptr<_vkarray.Job>
            Job
        """
        op = self._createOp(spv, len(buffers), params,
                            local_size_x, local_size_y, local_size_z)
        size = buffers[0].size()
        return self.gpu.submit(op, [b.info() for b in buffers],
                               shape, params, semaphores)

    def flush(self, arrays: Iterable[Array]):
        """
        Flush buffers

        Parameters
        ----------
        arrays : iterable of Array
            Arrays to be flushed
        """
        self.gpu.flush([a.range() for a in arrays])

    def wait(self):
        """
        Wait All GPU Operations
        """
        self.gpu.wait()


class Array:
    _add = os.path.join(shader_dir, "add.spv")
    _sub = os.path.join(shader_dir, "sub.spv")
    _mul = os.path.join(shader_dir, "mul.spv")
    _div = os.path.join(shader_dir, "div.spv")
    _iadd = os.path.join(shader_dir, "iadd.spv")
    _isub = os.path.join(shader_dir, "isub.spv")
    _imul = os.path.join(shader_dir, "imul.spv")
    _idiv = os.path.join(shader_dir, "idiv.spv")
    _add_scalar = os.path.join(shader_dir, "add_scalar.spv")
    _sub_scalar = os.path.join(shader_dir, "sub_scalar.spv")
    _mul_scalar = os.path.join(shader_dir, "mul_scalar.spv")
    _div_scalar = os.path.join(shader_dir, "div_scalar.spv")
    _iadd_scalar = os.path.join(shader_dir, "iadd_scalar.spv")
    _isub_scalar = os.path.join(shader_dir, "isub_scalar.spv")
    _imul_scalar = os.path.join(shader_dir, "imul_scalar.spv")
    _idiv_scalar = os.path.join(shader_dir, "idiv_scalar.spv")
    _rsub_scalar = os.path.join(shader_dir, "rsub_scalar.spv")
    _rdiv_scalar = os.path.join(shader_dir, "rdiv_scalar.spv")
    _matmul = os.path.join(shader_dir, "matmul.spv")
    _max = os.path.join(shader_dir, "max.spv")
    _min = os.path.join(shader_dir, "min.spv")
    _imax = os.path.join(shader_dir, "imax.spv")
    _imin = os.path.join(shader_dir, "imin.spv")
    _max_scalar = os.path.join(shader_dir, "max_scalar.spv")
    _min_scalar = os.path.join(shader_dir, "min_scalar.spv")
    _imax_scalar = os.path.join(shader_dir, "imax_scalar.spv")
    _imin_scalar = os.path.join(shader_dir, "imin_scalar.spv")
    _abs = os.path.join(shader_dir, "abs.spv")
    _sign = os.path.join(shader_dir, "sign.spv")
    _iabs = os.path.join(shader_dir, "iabs.spv")
    _isign = os.path.join(shader_dir, "isign.spv")
    _sin = os.path.join(shader_dir, "sin.spv")
    _cos = os.path.join(shader_dir, "cos.spv")
    _tan = os.path.join(shader_dir, "tan.spv")
    _isin = os.path.join(shader_dir, "isin.spv")
    _icos = os.path.join(shader_dir, "icos.spv")
    _itan = os.path.join(shader_dir, "itan.spv")
    _asin = os.path.join(shader_dir, "asin.spv")
    _acos = os.path.join(shader_dir, "acos.spv")
    _atan = os.path.join(shader_dir, "atan.spv")
    _iasin = os.path.join(shader_dir, "iasin.spv")
    _iacos = os.path.join(shader_dir, "iacos.spv")
    _iatan = os.path.join(shader_dir, "iatan.spv")
    _sinh = os.path.join(shader_dir, "sinh.spv")
    _cosh = os.path.join(shader_dir, "cosh.spv")
    _tanh = os.path.join(shader_dir, "tanh.spv")
    _isinh = os.path.join(shader_dir, "isinh.spv")
    _icosh = os.path.join(shader_dir, "icosh.spv")
    _itanh = os.path.join(shader_dir, "itanh.spv")
    _asinh = os.path.join(shader_dir, "asinh.spv")
    _acosh = os.path.join(shader_dir, "acosh.spv")
    _atanh = os.path.join(shader_dir, "atanh.spv")
    _iasinh = os.path.join(shader_dir, "iasinh.spv")
    _iacosh = os.path.join(shader_dir, "iacosh.spv")
    _iatanh = os.path.join(shader_dir, "iatanh.spv")
    _exp = os.path.join(shader_dir, "exp.spv")
    _log = os.path.join(shader_dir, "log.spv")
    _iexp = os.path.join(shader_dir, "iexp.spv")
    _ilog = os.path.join(shader_dir, "ilog.spv")
    _exp2 = os.path.join(shader_dir, "exp2.spv")
    _log2 = os.path.join(shader_dir, "log2.spv")
    _iexp2 = os.path.join(shader_dir, "iexp2.spv")
    _ilog2 = os.path.join(shader_dir, "ilog2.spv")
    _sqrt = os.path.join(shader_dir, "sqrt.spv")
    _invsqrt = os.path.join(shader_dir, "invsqrt.spv")
    _isqrt = os.path.join(shader_dir, "isqrt.spv")
    _iinvsqrt = os.path.join(shader_dir, "iinvsqrt.spv")
    _pow = os.path.join(shader_dir, "pow.spv")
    _ipow = os.path.join(shader_dir, "ipow.spv")
    _pow_scalar = os.path.join(shader_dir, "pow_scalar.spv")
    _ipow_scalar = os.path.join(shader_dir, "ipow_scalar.spv")
    _rpow_scalar = os.path.join(shader_dir, "rpow_scalar.spv")
    _clamp = os.path.join(shader_dir, "clamp.spv")
    _iclamp = os.path.join(shader_dir, "iclamp.spv")
    _clamp_sv = os.path.join(shader_dir, "clamp_sv.spv")
    _iclamp_sv = os.path.join(shader_dir, "iclamp_sv.spv")
    _clamp_vs = os.path.join(shader_dir, "clamp_vs.spv")
    _iclamp_vs = os.path.join(shader_dir, "iclamp_vs.spv")
    _clamp_ss = os.path.join(shader_dir, "clamp_ss.spv")
    _iclamp_ss = os.path.join(shader_dir, "iclamp_ss.spv")

    def __init__(self, gpu: GPU, *, data = None, shape = None):
        """
        Array for float (32bit)

        Parameters
        ----------
        gpu : GPU
            GPU instance to allocate at.
        data : array_like, optional
            Data which copy to GPU buffer.
        shape : array_like, optional
            Array shape

        Raises
        ------
        ValueError
            If both ``data`` and ``shape`` are ``None``.
        """
        self._gpu = gpu

        if data is not None:
            self.shape = np.asarray(data).shape
            self.buffer = self._gpu.gpu.toBuffer(np.ravel(data))
        elif shape is not None:
            self.shape = np.asarray(shape)
            self.buffer = self._gpu.gpu.createBuffer(int(self.shape.prod()))
        else:
            raise ValueError(f"`data` or `shape` must not be `None`.")

        self.array = np.asarray(self.buffer)
        self.array.shape = self.shape
        self.job = None

    def _check_shape(self, other):
        if not np.array_equal(self.shape, other.shape):
            raise ValueError(f"Incompatible shapes: {self.shape} vs {other.shape}")

    def _opVec(self, spv, buffers):
        size = self.buffer.size()
        return self._gpu._submit(spv, 64, 1, 1,
                                 [b.buffer for b in buffers],
                                 _vkarray.DataShape(size, 1, 1),
                                 _vkarray.VectorParams(size),
                                 [b.job.getSemaphore() for b in buffers
                                  if b.job is not None])

    def _opVec3(self, spv, other):
        self._check_shape(other)
        ret = Array(self._gpu, shape=self.shape)
        ret.job = self._opVec(spv, [self, other, ret])
        return ret

    def _opVec2(self, spv, other=None):
        if other is not None:
            self._check_shape(other)
            self.job = self._opVec(spv, [self, other])
        else:
            ret = Array(self._gpu, shape=self.shape)
            ret.job = self._opVec(spv, [self, ret])
            return ret

    def _opVec1(self, spv):
        self.job = self._opVec(spv, [self])

    def _opVecScalar(self, spv, buffers, scalar):
        size = self.buffer.size()
        return self._gpu._submit(spv, 64, 1, 1,
                                 [b.buffer for b in buffers],
                                 _vkarray.DataShape(size, 1, 1),
                                 _vkarray.VectorScalarParams(size, scalar),
                                 [b.job.getSemaphore() for b in buffers
                                  if b.job is not None])

    def _opVecScalar2(self, spv, other):
        ret = Array(self._gpu, shape=self.shape)
        ret.job = self._opVecScalar(spv, [self, ret], other)
        return ret

    def _opVecScalar1(self, spv, other):
        self.job = self._opVecScalar(spv, [self], other)

    def _opVec2Scalar(self, spv, buffers, scalars):
        size = self.buffer.size()
        return self._gpu._submit(spv, 64, 1, 1,
                                 [b.buffer for b in buffers],
                                 _vkarray.DataShape(size, 1, 1),
                                 _vkarray.VectorScalar2Params(size, *scalars),
                                 [b.job.getSemaphore() for b in buffers
                                  if b.job is not None])

    def __add__(self, other: Union[Self, float]) -> Array:
        if isinstance(other, Array):
            return self._opVec3(self._add, other)
        else:
            return self._opVecScalar2(self._add_scalar, other)

    def __sub__(self, other: Union[Self, float]) -> Array:
        if isinstance(other, Array):
            return self._opVec3(self._sub, other)
        else:
            return self._opVecScalar2(self._sub_scalar, other)

    def __mul__(self, other: Union[Self, float]) -> Array:
        if isinstance(other, Array):
            return self._opVec3(self._mul, other)
        else:
            return self._opVecScalar2(self._mul_scalar, other)

    def __truediv__(self, other: Union[Self, float]) -> Array:
        if isinstance(other, Array):
            return self._opVec3(self._div, other)
        else:
            return self._opVecScalar2(self._div_scalar, other)

    def __iadd__(self, other: Union[Self, float]) -> Array:
        if isinstance(other, Array):
            self._opVec2(self._iadd, other)
        else:
            self._opVecScalar1(self._iadd_scalar, other)
        return self

    def __isub__(self, other: Union[Self, float]) -> Array:
        if isinstance(other, Array):
            self._opVec2(self._isub, other)
        else:
            self._opVecScalar1(self._isub_scalar, other)
        return self

    def __imul__(self, other: Union[Self, float]) -> Array:
        if isinstance(other, Array):
            self._opVec2(self._imul, other)
        else:
            self._opVecScalar1(self._imul_scalar, other)
        return self

    def __itruediv__(self, other: Union[Self, float]) -> Array:
        if isinstance(other, Array):
            self._opVec2(self._idiv, other)
        else:
            self._opVecScalar1(self._idiv_scalar, other)
        return self

    def __radd__(self, other: float) -> Array:
        return self._opVecScalar2(self._add_scalar, other)

    def __rsub__(self, other: float) -> Array:
        return self._opVecScalar2(self._rsub_scalar, other)

    def __rmul__(self, other: float) -> Array:
        return self._opVecScalar2(self._mul_scalar, other)

    def __rtruediv__(self, other: float) -> Array:
        return self._opVecScalar2(self._rdiv_scalar, other)

    def __matmul__(self, other: Array) -> Array:
        if ((len(self.shape) > 3) or
            (len(other.shape) > 3) or
            (self.shape[-1] != other.shape[0])):
            raise ValueError(f"Incompatible shapes: {self.shape} vs {other.shape}")

        shape = tuple(self.shape)[:-1] + tuple(other.shape)[1:]
        if len(shape) == 0:
            shape = (1,)

        rowA = self.shape[0] if len(self.shape) > 1 else 1
        contractSize = self.shape[-1]
        columnB = other.shape[1] if len(other.shape) > 1 else 1

        ret = Array(self._gpu, shape=shape)
        ret.job = self._gpu._submit(self._matmul, 1, 64, 1,
                                    [self.buffer, other.buffer, ret.buffer],
                                    _vkarray.DataShape(rowA, columnB, 1),
                                    _vkarray.MatMulParams(rowA,contractSize,columnB),
                                    [b.job.getSemaphore() for b in [self, other]
                                     if b.job is not None])
        return ret

    def wait(self):
        """
        Wait Last Job
        """
        if self.job is not None:
            self.job.wait()
            self.job = None

    def flush(self):
        """
        Flush Buffer to GPU
        """
        self._gpu.flush([self])

    def __getitem__(self, key) -> Union[float, np.ndarray]:
        self.wait()
        return self.array[key]

    def __setitem__(self, key, value):
        self.array[key] = value

    def __repr__(self) -> str:
        return f"<vulkpy.Buffer(shape={tuple(self.shape)})>"

    def __str__(self) -> str:
        self.wait()
        return str(self.array)

    def __array__(self) -> np.ndarray:
        self.wait()
        return self.array

    def reshape(self, shape: tuple[int]):
        """
        Reshape of this array

        Parameters
        ----------
        shape : tuple of int
            New shape

        Raises
        ------
        ValueError
            If ``shape`` is incompatible
        """
        self.array.shape = shape
        self.shape = self.array.shape

    def max(self, other: Union[Array, float],
            inplace: bool = False) -> Optional[Array]:
        """
        Element-wise Max

        Parameters
        ----------
        other : Array or float
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.

        Raises
        ------
        ValueError
            If shape is not same.
        """
        if isinstance(other, Array):
            if inplace:
                self._opVec2(self._imax, other)
            else:
                return self._opVec3(self._max, other)
        else:
            if inplace:
                self._opVecScalar1(self._imax_scalar, other)
            else:
                return self._opVecScalar2(self._max_scalar, other)

    def min(self, other: Union[Array, float],
            inplace: bool = False) -> Optional[Array]:
        """
        Element-wise Min

        Parameters
        ----------
        other : Array or float
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.

        Raises
        ------
        ValueError
            If shape is not same.
        """
        if isinstance(other, Array):
            if inplace:
                self._opVec2(self._imin, other)
            else:
                return self._opVec3(self._min, other)
        else:
            if inplace:
                self._opVecScalar1(self._imin_scalar, other)
            else:
                return self._opVecScalar2(self._min_scalar, other)

    def abs(self, inplace: bool = False) -> Optional[Array]:
        """
        Element-wise Abs

        Parameters
        ----------
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        if inplace:
            self._opVec1(self._iabs)
        else:
            return self._opVec2(self._abs)

    def sign(self, inplace: bool = False) -> Optional[Array]:
        """
        Element-wise sign

        Parameters
        ----------
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        if inplace:
            self._opVec1(self._isign)
        else:
            return self._opVec2(self._sign)

    def sin(self, inplace: bool = False) -> Optional[Array]:
        """
        Element-wise sin()

        Parameters
        ----------
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        if inplace:
            self._opVec1(self._isin)
        else:
            return self._opVec2(self._sin)

    def cos(self, inplace: bool = False) -> Optional[Array]:
        """
        Element-wise cos()

        Parameters
        ----------
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        if inplace:
            self._opVec1(self._icos)
        else:
            return self._opVec2(self._cos)

    def tan(self, inplace: bool = False) -> Optional[Array]:
        """
        Element-wise tan()

        Parameters
        ----------
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        if inplace:
            self._opVec1(self._itan)
        else:
            return self._opVec2(self._tan)

    def asin(self, inplace: bool = False) -> Optional[Array]:
        """
        Element-wise asin()

        Parameters
        ----------
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        if inplace:
            self._opVec1(self._iasin)
        else:
            return self._opVec2(self._asin)

    def acos(self, inplace: bool = False) -> Optional[Array]:
        """
        Element-wise acos()

        Parameters
        ----------
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        if inplace:
            self._opVec1(self._iacos)
        else:
            return self._opVec2(self._acos)

    def atan(self, inplace: bool = False) -> Optional[Array]:
        """
        Element-wise atan()

        Parameters
        ----------
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        if inplace:
            self._opVec1(self._iatan)
        else:
            return self._opVec2(self._atan)

    def sinh(self, inplace: bool = False) -> Optional[Array]:
        """
        Element-wise sinh()

        Parameters
        ----------
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        if inplace:
            self._opVec1(self._isinh)
        else:
            return self._opVec2(self._sinh)

    def cosh(self, inplace: bool = False) -> Optional[Array]:
        """
        Element-wise cosh()

        Parameters
        ----------
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        if inplace:
            self._opVec1(self._icosh)
        else:
            return self._opVec2(self._cosh)

    def tanh(self, inplace: bool = False) -> Optional[Array]:
        """
        Element-wise tanh()

        Parameters
        ----------
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        if inplace:
            self._opVec1(self._itanh)
        else:
            return self._opVec2(self._tanh)

    def asinh(self, inplace: bool = False) -> Optional[Array]:
        """
        Element-wise asinh()

        Parameters
        ----------
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        if inplace:
            self._opVec1(self._iasinh)
        else:
            return self._opVec2(self._asinh)

    def acosh(self, inplace: bool = False) -> Optional[Array]:
        """
        Element-wise acosh()

        Parameters
        ----------
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        if inplace:
            self._opVec1(self._iacosh)
        else:
            return self._opVec2(self._acosh)

    def atanh(self, inplace: bool = False) -> Optional[Array]:
        """
        Element-wise atanh()

        Parameters
        ----------
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        if inplace:
            self._opVec1(self._iatanh)
        else:
            return self._opVec2(self._atanh)

    def exp(self, inplace: bool = False) -> Optional[Array]:
        """
        Element-wise exp()

        Parameters
        ----------
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        if inplace:
            self._opVec1(self._iexp)
        else:
            return self._opVec2(self._exp)

    def log(self, inplace: bool = False) -> Optional[Array]:
        """
        Element-wise log()

        Parameters
        ----------
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        if inplace:
            self._opVec1(self._ilog)
        else:
            return self._opVec2(self._log)

    def exp2(self, inplace: bool = False) -> Optional[Array]:
        """
        Element-wise exp2()

        Parameters
        ----------
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        if inplace:
            self._opVec1(self._iexp2)
        else:
            return self._opVec2(self._exp2)

    def log2(self, inplace: bool = False) -> Optional[Array]:
        """
        Element-wise log2()

        Parameters
        ----------
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        if inplace:
            self._opVec1(self._ilog2)
        else:
            return self._opVec2(self._log2)

    def sqrt(self, inplace: bool = False) -> Optional[Array]:
        """
        Element-wise sqrt()

        Parameters
        ----------
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        if inplace:
            self._opVec1(self._isqrt)
        else:
            return self._opVec2(self._sqrt)

    def invsqrt(self, inplace: bool = False) -> Optional[Array]:
        """
        Element-wise 1/sqrt()

        Parameters
        ----------
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        if inplace:
            self._opVec1(self._iinvsqrt)
        else:
            return self._opVec2(self._invsqrt)

    def __pow__(self, other: Union[Array, float]) -> Array:
        if isinstance(other, Array):
            return self._opVec3(self._pow, other)
        else:
            return self._opVecScalar2(self._pow_scalar, other)

    def __ipow__(self, other: Union[Array, float]) -> Array:
        if isinstance(other, Array):
            self._opVec2(self._ipow, other)
        else:
            self._opVecScalar1(self._ipow_scalar, other)
        return self

    def __rpow__(self, other: float) -> Array:
        return self._opVecScalar2(self._rpow_scalar, other)

    def clamp(self, min: Union[Array, float], max: Union[Array, float],
              inplace: bool = False) -> Optional[Array]:
        """
        Element-wise clamp()

        Parameters
        ----------
        min, max : Array or float
            Minimum/Maximum value
        inplace : bool
            If ``True``, update inplace, otherwise returns new array.
            Default value is ``False``.

        Returns
        -------
        None
            When ``replace=True``.
        Array
            When ``replace=False``.
        """
        min_is_array = isinstance(min, Array)
        if min_is_array:
            self._check_shape(min)

        max_is_array = isinstance(max, Array)
        if max_is_array:
            self._check_shape(max)

        if not inplace:
            ret = Array(self._gpu, shape=self.shape)
            if min_is_array and max_is_array:
                ret.job = self._opVec(self._clamp, [self, min, max, ret])
            elif max_is_array:
                ret.job = self._opVecScalar(self._clamp_sv, [self, max, ret], min)
            elif min_is_array:
                ret.job = self._opVecScalar(self._clamp_vs, [self, min, ret], max)
            else:
                ret.job = self._opVec2Scalar(self._clamp_ss, [self, ret], [min, max])
            return ret
        else:
            # inplace
            if min_is_array and max_is_array:
                self.job = self._opVec(self._iclamp, [self, min, max])
            elif max_is_array:
                self.job = self._opVecScalar(self._iclamp_sv, [self, max], min)
            elif min_is_array:
                self.job = self._opVecScalar(self._iclamp_vs, [self, min], max)
            else:
                self.job = self._opVec2Scalar(self._iclamp_ss, [self], [min, max])
