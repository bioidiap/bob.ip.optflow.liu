/**
 * @author Andre Anjos <andre.anjos@idiap.ch>
 * @date Thu  3 Apr 09:02:51 2014 CEST
 *
 * @brief Bob/Python extension to Ce Liu's Optical Flow dense estimator using
 * Conjugate-Gradient for minimization (old version).
 */

#ifdef NO_IMPORT_ARRAY
#undef NO_IMPORT_ARRAY
#endif
#include <bob.blitz/capi.h>
#include <bob.blitz/cleanup.h>

#include "OpticalFlow.h"

/**
 * Temporarily assigns the memory storage from the blitz array to the double
 * image type that is used by Liu's framework.
 */
static void bz2dimage(PyBlitzArrayObject* bz, cg::DImage& di) {
  di.clear();
  if (bz->ndim == 2) {
    di.imWidth = bz->shape[1];
    di.imHeight = bz->shape[0];
    di.nChannels = 1;
    di.computeDimension();
    di.pData = reinterpret_cast<double*>(bz->data);
  }
  else {
    di.ConvertFromMatlab<double>(reinterpret_cast<double*>(bz->data),
        bz->shape[2], bz->shape[1], bz->shape[0]);
  }
}

static PyObject* coarse2fine_flow (
    PyBlitzArrayObject* i1, //first input image
    PyBlitzArrayObject* i2, //second input image
    double alpha=0.02,
    double ratio=0.75,
    int minWidth=30,
    int nOuterFPIterations=20,
    int nInnerFPIterations=1,
    int nCGIterations=50
    ) {

  cg::DImage di1;
  cg::DImage di2;

  //Maps input images
  bz2dimage(i1, di1);
  bz2dimage(i2, di2);

  //Output arrays
  cg::DImage du;
  cg::DImage dv;
  cg::DImage dwarped_i2;

  //Calls Optical Flow estimation
  Py_BEGIN_ALLOW_THREADS
  cg::OpticalFlow::Coarse2FineFlow(du, dv, dwarped_i2, di1, di2,
      alpha, ratio, minWidth, nOuterFPIterations, nInnerFPIterations,
      nCGIterations);
  Py_END_ALLOW_THREADS

  if (i1->ndim == 2) {
    //Resets input images so we don't get a delete on those
    di1.pData = 0;
    di2.pData = 0;
  }
  //else { for info.nd == 3 we do have to delete! }

  //Copies output data back
  Py_ssize_t* shape = i1->shape;
  if (i1->ndim == 3) shape += 1; //use the last two indices

  PyObject* u = PyArray_SimpleNew(2, shape, NPY_FLOAT64);
  if (!u) return 0;
  auto u_ = make_safe(u);
  void* u_data = PyArray_DATA((PyArrayObject*)u);
  memcpy(u_data, du.pData, sizeof(double)*du.nElements);

  PyObject* v = PyArray_SimpleNew(2, shape, NPY_FLOAT64);
  if (!v) return 0;
  auto v_ = make_safe(v);
  void* v_data = PyArray_DATA((PyArrayObject*)v);
  memcpy(v_data, dv.pData, sizeof(double)*dv.nElements);

  PyObject* w2 = PyArray_SimpleNew(i2->ndim, i2->shape, NPY_FLOAT64);
  if (!w2) return 0;
  auto w2_ = make_safe(w2);
  void* w2_data = PyArray_DATA((PyArrayObject*)w2);

  if (i1->ndim == 2) {
    memcpy(w2_data, dwarped_i2.pData, sizeof(double)*dwarped_i2.nElements);
  }
  else {
    dwarped_i2.ConvertToMatlab(reinterpret_cast<double*>(w2_data));
  }

  return Py_BuildValue("(OOO)", u, v, w2);
}

PyDoc_STRVAR(s_flow_str, "flow");
PyDoc_STRVAR(s_flow_doc,
"flow(i1, i2, [alpha=0.02, [ratio=0.75, [min_width=30, [n_outer_fp_iterations=20, [n_inner_fp_iterations=1, [n_cg_iterations=50]]]]]]) -> (u, v, w2)\n\
\n\
This method computes the dense optical flow field using a\n\
coarse-to-fine approach. C++ code running under this call is\n\
extracted from **the old version (pre Aug 1, 2011)** of\n\
`Ce Liu's homepage\n\
<http://people.csail.mit.edu/celiu/OpticalFlow/>`_ and should\n\
give the exact same output as the Matlab equivalent.\n\
\n\
.. note::\n\
\n\
   This variant does not use the Successive Over-Relaxation\n\
   (SOR) that was implemented on August 1st., 2011 by C. Liu,\n\
   but the old version based on Conjugate-Gradient (CG).\n\
\n\
Parameters:\n\
\n\
i1\n\
  First input frame (grayscale/double image)\n\
\n\
i2\n\
  Second input frame (same dimension and type of the first frame)\n\
\n\
alpha\n\
  [optional] Regularization weight\n\
\n\
ratio\n\
  [optional] Downsample ratio\n\
\n\
min_width\n\
  [optional] Width of the coarsest level\n\
\n\
n_outer_fp_iterations\n\
  [optional] The number of outer fixed point iterations\n\
\n\
n_inner_fp_iterations\n\
  [optional] The number of inner fixed point iterations\n\
\n\
n_cg_iterations\n\
  [optional] The number of conjugate-gradient (CG) iterations\n\
\n\
Returns a tuple containing three 2D double arrays with the same\n\
dimensions as the input images:\n\
\n\
u\n\
  Output velocities in ``x`` (horizontal axis).\n\
\n\
v\n\
  Output velocities in ``y`` (vertical axis).\n\
\n\
warped_i2\n\
  i2 as estimated by the optical flow field from i1\n\
\n\
");

PyObject* flow(PyObject*, PyObject* args, PyObject* kwds) {

  /* Parses input arguments in a single shot */
  static const char* const_kwlist[] = {
    "i1",
    "i2",
    "alpha",
    "ratio",
    "min_width",
    "n_outer_fp_iterations",
    "n_inner_fp_iterations",
    "n_cg_iterations",
    0
  };
  static char** kwlist = const_cast<char**>(const_kwlist);

  PyBlitzArrayObject* i1 = 0;
  PyBlitzArrayObject* i2 = 0;
  double alpha = 0.02;
  double ratio = 0.75;
  Py_ssize_t min_width = 30;
  Py_ssize_t n_outer_fp_iterations = 20;
  Py_ssize_t n_inner_fp_iterations = 1;
  Py_ssize_t n_cg_iterations = 50;

  if (!PyArg_ParseTupleAndKeywords(args, kwds, "O&O&|ddnnnn", kwlist,
        &PyBlitzArray_Converter, &i1,
        &PyBlitzArray_Converter, &i2,
        &alpha,
        &ratio,
        &min_width,
        &n_outer_fp_iterations,
        &n_inner_fp_iterations,
        &n_cg_iterations
        ))
    return 0;

  PyBlitzArrayObject* tmp = 0;

  //make sure i1 is convertible to float64
  tmp = (PyBlitzArrayObject*)PyBlitzArray_Cast(i1, NPY_FLOAT64);
  Py_DECREF(i1);
  i1 = tmp;
  if (!i1) return 0;
  auto i1_ = make_safe(i1);

  //make sure i2 is convertible to float64
  tmp = (PyBlitzArrayObject*)PyBlitzArray_Cast(i2, NPY_FLOAT64);
  Py_DECREF(i2);
  i2 = tmp;
  if (!i2) return 0;
  auto i2_ = make_safe(i2);

  //some checks
  if (i1->ndim != 2 && i1->ndim != 3) {
    PyErr_Format(PyExc_TypeError, "method only supports 2D or 3D arrays for input image `i1', but you passed an array with %" PY_FORMAT_SIZE_T "d dimensions", i1->ndim);
    return 0;
  }

  if (i1->ndim != i2->ndim) {
    PyErr_Format(PyExc_TypeError, "input image arrays must have the same number of dimensions, but image `i1' has %" PY_FORMAT_SIZE_T "d dimensions while image `i2' has %" PY_FORMAT_SIZE_T "d", i1->ndim, i2->ndim);
    return 0;
  }

  if (i1->ndim == 2) {
    if (i1->shape[0] != i2->shape[0] || i2->shape[1] != i2->shape[1]) {
    PyErr_Format(PyExc_RuntimeError, "shapes of the input images differ: (%" PY_FORMAT_SIZE_T "d, %" PY_FORMAT_SIZE_T "d) != (%" PY_FORMAT_SIZE_T "d, %" PY_FORMAT_SIZE_T "d)", i1->shape[0], i1->shape[1], i2->shape[0], i2->shape[1]);
    return 0;
    }
  }
  else { //ndim == 3
    if (i1->shape[0] != i2->shape[0] || i2->shape[1] != i2->shape[1] ||
        i2->shape[2] != i2->shape[2]) {
      PyErr_Format(PyExc_RuntimeError, "shapes of the input images differ: (%" PY_FORMAT_SIZE_T "d, %" PY_FORMAT_SIZE_T "d, %" PY_FORMAT_SIZE_T "d) != (%" PY_FORMAT_SIZE_T "d, %" PY_FORMAT_SIZE_T "d, %" PY_FORMAT_SIZE_T "d)", i1->shape[0], i1->shape[1], i1->shape[2], i2->shape[0], i2->shape[1], i2->shape[2]);
      return 0;
    }
  }

  return coarse2fine_flow(i1, i2, alpha, ratio, min_width,
      n_outer_fp_iterations, n_inner_fp_iterations, n_cg_iterations);

}

static PyMethodDef module_methods[] = {
    {
      s_flow_str,
      (PyCFunction)flow,
      METH_VARARGS|METH_KEYWORDS,
      s_flow_doc
    },
    {0}  /* Sentinel */
};

PyDoc_STRVAR(module_docstr, "Ce Liu's Optical Flow implementations using CG");

#if PY_VERSION_HEX >= 0x03000000
static PyModuleDef module_definition = {
  PyModuleDef_HEAD_INIT,
  BOB_EXT_MODULE_NAME,
  module_docstr,
  -1,
  module_methods,
  0, 0, 0, 0
};
#endif

static PyObject* create_module (void) {

# if PY_VERSION_HEX >= 0x03000000
  PyObject* module = PyModule_Create(&module_definition);
  auto module_ = make_xsafe(module);
  const char* ret = "O";
# else
  PyObject* module = Py_InitModule3(BOB_EXT_MODULE_NAME, module_methods, module_docstr);
  const char* ret = "N";
# endif
  if (!module) return 0;

  /* imports dependencies */
  if (import_bob_blitz() < 0) return 0;

  return Py_BuildValue(ret, module);
}

PyMODINIT_FUNC BOB_EXT_ENTRY_NAME (void) {
# if PY_VERSION_HEX >= 0x03000000
  return
# endif
    create_module();
}
