bool skipHBChannel(int iphi,int ieta) {
  if (
      (ieta==-2 && iphi==2) ||
      (ieta==-6  && iphi==2) || 
      (ieta==-10  && iphi==2) ||
      (ieta==-13  && iphi==7) ||
      (ieta==14  && iphi==31) ||
      ((iphi==54 || iphi==51 || iphi==52) && ieta>0 && ieta<17)
      )
    return true;
  else return false;
}
