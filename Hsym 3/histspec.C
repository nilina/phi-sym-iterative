void histspec(TH1* hist, Double_t &mean, Double_t &ermean, Double_t &rms, 
		Double_t range=4, Double_t rangef=2.5, int mode=0) {

  Double_t xmin,xmax,rmsmin,meanf,ermeanf,rmsf;
  char ctit[145];

  mean=hist->GetMean();
  rms=hist->GetRMS();
  xmin=hist->GetXaxis()->GetXmin();
  xmax=hist->GetXaxis()->GetXmax();
  int nb=hist->GetNbinsX();
  rmsmin=(xmax-xmin)/(nb+1);
  if (rms==0) rms=rmsmin;

  for (int i=0;i<2;i++) {
    hist->SetAxisRange(mean-range*rms,mean+range*rms);
    mean=hist->GetMean();
    rms=hist->GetRMS();
    if (rms==0) rms=rmsmin;
  }
  
  if (rangef>0) {
    for (int i=0;i<2;i++) {
      hist->SetAxisRange(mean-rangef*rms,mean+rangef*rms);
      mean=hist->GetMean();
      rms=hist->GetRMS();
      if (rms==0) rms=rmsmin;
    }
  }
  
  ermean=hist->GetMeanError();
  if (abs(mode)>0) {
    if (mode<0) {
      //sprintf(ctit,"cHistSpecs%4d",nHistSpecs++);
      //TCanvas *ccxx = new TCanvas("ccxx","ccxx",900,0,450,450);
      //hist->SetMinimum(0);
      //hist->Draw();
      hist->Fit("gaus","LI","same",mean-rangef*rms,mean+rangef*rms);
      //ccxx->Update();
      for (int i=0;i<1e3;i++) for (int j=0;j<1e3;j++) {} 
    }
    else hist->Fit("gaus","LI0","",mean-rangef*rms,mean+rangef*rms);
    TF1 *f = hist->GetFunction("gaus");
    meanf=f->GetParameter(1);
    ermeanf=f->GetParError(1);
    rmsf=f->GetParameter(2);
    if (fabs(mean-meanf)/(fabs(mean+meanf)+0.0001)<0.8 && 
	fabs(ermean-ermeanf)/(fabs(ermean+ermeanf)+0.0001)<0.8) {
      mean=meanf;
      ermean=ermeanf;
      rms=rmsf;
    }
  }
  hist->SetAxisRange(xmin,xmax);
  return;
}

