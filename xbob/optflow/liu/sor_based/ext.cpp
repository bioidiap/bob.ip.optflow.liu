/**
 * @author Andre Anjos <andre.anjos@idiap.ch>
 * @date Thu 08 Nov 2012 12:09:32 CET 
 *
 * @brief Boost.Python extension to Ce Liu's Optical Flow dense estimator
 */

#include <boost/python.hpp>

#include <bob/config.h>
#ifdef BOB_API_VERSION
#  include <bob/python/gil.h>
#  include <bob/python/ndarray.h>
#else
#  include <bob/core/python/gil.h>
#  include <bob/core/python/ndarray.h>
#endif

#include "OpticalFlow.h"

using namespace boost::python;

/**
 * Temporarily assigns the memory storage from the blitz array to the double
 * image type that is used by Liu's framework.
 */
static void bz2dimage(blitz::Array<double,2>& bz, sor::DImage& di) {
  di.clear();
  di.imWidth = bz.extent(1);
  di.imHeight = bz.extent(0);
  di.nChannels = 1;
  di.colorType = sor::GRAY;
  di.computeDimension();
  di.pData = bz.data();
}

/**
 * Copies and transposes 3D array data
 */
static void bz2dimage(blitz::Array<double,3>& bz, sor::DImage& di) {
  di.clear();
  di.colorType = sor::RGB;
  di.ConvertFromMatlab<double>(bz.data(), bz.extent(2), bz.extent(1),
      bz.extent(0));
}

static tuple coarse2fine_flow (
    bob::python::const_ndarray i1, //first input image
    bob::python::const_ndarray i2, //second input image
    double alpha=1.0,
    double ratio=0.5,
    int minWidth=40,
    int nOuterFPIterations=4,
    int nInnerFPIterations=1,
    int nSORIterations=20
    ) {

  bob::core::array::typeinfo info = i1.type();
  sor::DImage di1;
  sor::DImage di2;

  if (info.nd == 2) {

    //Checks Im1 and Im2 are convertible into double/grayscaled images
    blitz::Array<double,2> bz1 = i1.cast<double,2>();
    blitz::Array<double,2> bz2 = i2.cast<double,2>();

    if (bz1.extent(0) != bz2.extent(0) || 
        bz1.extent(1) != bz2.extent(1)) {
      throw std::runtime_error("shapes of input images differ");
    }

    //Maps input images
    bz2dimage(bz1, di1);
    bz2dimage(bz2, di2);

  }
  else {

    //Checks Im1 and Im2 are convertible into double/grayscaled images
    blitz::Array<double,3> bz1 = i1.cast<double,3>();
    blitz::Array<double,3> bz2 = i2.cast<double,3>();

    if (bz1.extent(0) != bz2.extent(0) || 
        bz1.extent(1) != bz2.extent(1) ||
        bz1.extent(2) != bz2.extent(2)) {
      throw std::runtime_error("shapes of input images differ");
    }

    //Maps input images
    bz2dimage(bz1, di1);
    bz2dimage(bz2, di2);

  }

  //Output arrays
  sor::DImage du;
  sor::DImage dv;
  sor::DImage dwarped_i2;

  //Calls Optical Flow estimation
  sor::OpticalFlow::Coarse2FineFlow(du, dv, dwarped_i2, di1, di2,
      alpha, ratio, minWidth, nOuterFPIterations, nInnerFPIterations,
      nSORIterations);

  if (info.nd == 2) {
    //Resets input images so we don't get a delete on those
    di1.pData = 0;
    di2.pData = 0;
  }
  //else { for info.nd == 3 we do have to delete! }

  //Copies output data back
  tuple retval;
  
  bob::python::py_array u(bob::core::array::t_float64, di1.imHeight, di1.imWidth);
  memcpy(u.ptr(), du.pData, sizeof(double)*du.nElements);
  bob::python::py_array v(bob::core::array::t_float64, di1.imHeight, di1.imWidth);
  memcpy(v.ptr(), dv.pData, sizeof(double)*dv.nElements);

  if (info.nd == 2) {

    bob::python::py_array w2(bob::core::array::t_float64, di1.imHeight, di1.imWidth);
    memcpy(w2.ptr(), dwarped_i2.pData, sizeof(double)*dwarped_i2.nElements);
    retval = make_tuple(u.pyobject(), v.pyobject(), w2.pyobject());

  }

  else {

    bob::python::py_array w2(bob::core::array::t_float64, di1.nChannels, di1.imHeight, di1.imWidth);
    dwarped_i2.ConvertToMatlab(static_cast<double*>(w2.ptr()));
    retval = make_tuple(u.pyobject(), v.pyobject(), w2.pyobject());

  }

  return retval;
}

namespace sor {
  BOOST_PYTHON_FUNCTION_OVERLOADS(coarse2fine_flow_overloads, coarse2fine_flow, 2, 8)
}

BOOST_PYTHON_MODULE(_sor_based) {
  bob::python::setup_python("Bindings to Ce Liu's Optical Flow dense estimator (using Successive-Over-Relaxation)");

  boost::python::def("flow", coarse2fine_flow, sor::coarse2fine_flow_overloads((
          boost::python::arg("i1"), 
          boost::python::arg("i2"), 
          boost::python::arg("alpha")=1.0, 
          boost::python::arg("ratio")=0.5, 
          boost::python::arg("min_width")=40, 
          boost::python::arg("n_outer_fp_iterations")=4, 
          boost::python::arg("n_inner_fp_iterations")=1,
          boost::python::arg("n_sor_iterations")=20), 
        "Computes dense optical flow field in a coarse to fine manner\n"
        "\n"
        "This method computes the dense optical flow field using a coarse-to-fine approach. C++ code running under this call is extracted from `Ce Liu's homepage <http://people.csail.mit.edu/celiu/OpticalFlow/>`_ and should give the exact same output as the Matlab equivalent.\n\n"
        "Keyword Parameters:\n"
        "\n"
        "i1\n"
        "  First input frame (grayscale/double image)\n"
        "i2\n"
        "  Second input frame (same dimension and type of the first frame)\n"
        "alpha\n"
        "  [optional] Regularization weight\n"
        "ratio\n"
        "  [optional] Downsample ratio\n"
        "min_width\n"
        "  [optional] Width of the coarsest level\n"
        "n_outer_fp_iterations\n"
        "  [optional] The number of outer fixed point iterations\n"
        "n_inner_fp_iterations\n"
        "  [optional] The number of inner fixed point iterations\n"
        "n_sor_iterations\n"
        "  [optional] The number of successive over-relaxation (SOR) iterations\n"
        "\n"
        "Returns a tuple containing three 2D double arrays with the same dimensions as the input images:\n"
        "\n"
        "u\n"
        "  Output velocities in ``x`` (horizontal axis).\n"
        "v\n"
        "  Output velocities in ``y`` (vertical axis).\n"
        "warped_i2\n"
        "  i2 as estimated by the optical flow field from i1\n"
        )
        );
}
