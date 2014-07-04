#include <vector>
#include <exception>
#include "TRandom.h"
#include "TStyle.h"
#include "TFile.h"
#include "TTree.h"
#include "TMath.h"
#include "TF1.h"
#include "TH1.h"
#include "TH2.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TProfile.h"
#include "TCanvas.h"
#include "Riostream.h"
#include "TLatex.h"
#include "TColor.h"
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include "histspec.C"

void histStat(TH1F* h, int mode=0) {

  TLatex tt0, tt1, tt2, tt3, tt4, tt5;
  tt0.SetTextFont(42);
  tt0.SetTextAlign(11);
  tt0.SetTextColor(1);
  tt0.SetTextSize(0.06);
  tt3.SetTextFont(42);
  tt3.SetTextAlign(11);
  tt3.SetTextColor(4);
  tt3.SetTextSize(0.045);
  tt3.SetTextAngle(0);
  tt2.SetTextFont(42);
  tt2.SetTextAlign(11);
  tt2.SetTextColor(2);
  tt2.SetTextSize(0.045);
  tt2.SetTextAngle(0);
  tt1.SetTextFont(42);
  tt1.SetTextAlign(11);
  tt1.SetTextColor(1);
  tt1.SetTextSize(0.045);
  tt1.SetTextAngle(0);
  tt4.SetTextFont(42);
  tt4.SetTextAlign(11);
  tt4.SetTextColor(1);
  tt4.SetTextSize(0.043);
  tt4.SetTextAngle(0);
  tt5.SetTextFont(42);
  tt5.SetTextAlign(11);
  tt5.SetTextColor(3);
  tt5.SetTextSize(0.04);
  tt5.SetTextAngle(0);

  char ctit[128];

  double    ahmax=h->GetMaximum();
  double    mean=h->GetMean();
  double    ermean=h->GetMeanError();
  double    rms=h->GetRMS();

  Int_t nx = h->GetNbinsX();
  Double_t x1 = h->GetXaxis()->GetBinLowEdge(1);
  Double_t x2 = h->GetXaxis()->GetBinUpEdge(1);
  double dx = x2-x1;
  double x = x1 + dx*nx*0.5;

  sprintf(ctit,"Mean = %6.4f",h->GetMean());
  tt4.DrawLatex(x,ahmax*0.93,ctit);
  sprintf(ctit,"RMS = %6.4f",h->GetRMS());
  tt4.DrawLatex(x,ahmax*0.86,ctit);

  if (mode!=0) {
    histspec(h,mean,ermean,rms,3,-3);
    sprintf(ctit,"RMS(peak) = %6.4f",rms);
    tt4.DrawLatex(x,ahmax*0.79,ctit);
  }
}
