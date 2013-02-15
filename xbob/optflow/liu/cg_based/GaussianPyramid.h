#ifndef _GaussianPyramid_h
#define _GaussianPyramid_h

#include "Image.h"

namespace cg {

  class GaussianPyramid
  {
    private:
      DImage* ImPyramid;
      int nLevels;
    public:
      GaussianPyramid(void);
      ~GaussianPyramid(void);
      void ConstructPyramid(const DImage& image,double ratio=0.8,int minWidth=30);
      inline int nlevels() const {return nLevels;};
      inline DImage& Image(int index) {return ImPyramid[index];};
  };

}

#endif
