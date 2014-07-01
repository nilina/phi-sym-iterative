
import FWCore.ParameterSet.Config as cms

process = cms.Process("PHASEHFX")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 10000
process.MessageLogger.cerr.default.limit = 10

process.load('Configuration.StandardSequences.Services_cff')
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load("Configuration.StandardSequences.Reconstruction_cff")

#--- Global Tag conditions
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.autoCond import autoCond
#process.GlobalTag.globaltag = autoCond['mc'] #mc
process.GlobalTag.globaltag = autoCond['startup'] #data
#process.GlobalTag.globaltag = 'GR_E_V25::All'
#process.GlobalTag.globaltag = 'GR_R_52_V7::All'

process.es_pool = cms.ESSource("PoolDBESSource",  
                                process.CondDBSetup,
                                timetype = cms.string('runnumber'),
                                toGet = cms.VPSet(
     cms.PSet(
              record = cms.string("HcalRespCorrsRcd"),
              tag = cms.string("HcalRespCorrs_v4.5_offline")),
      cms.PSet(
             record = cms.string('HcalGainsRcd'),
             tag = cms.string('HcalGains_v5.07_offline')),

     ),
     connect = cms.string('frontier://FrontierProd/CMS_COND_31X_HCAL'),
     authenticationMethod = cms.untracked.uint32(0),
)
process.es_prefer_es_pool = cms.ESPrefer( "PoolDBESSource", "es_pool")

# summary
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False),
					SkipEvent = cms.untracked.vstring('ProductNotFound')
)

# BPTX & BSC triggers filter
process.load('L1TriggerConfig.L1GtConfigProducers.L1GtTriggerMaskTechTrigConfig_cff')
process.load("HLTrigger.HLTfilters.hltLevel1GTSeed_cfi")
process.hltLevel1GTSeed.L1TechTriggerSeeding = cms.bool(True)
process.hltLevel1GTSeed.L1SeedsLogicalExpression = cms.string('NOT (36 OR 37 OR 38 OR 39) AND NOT ((42 AND NOT 43) OR (43 AND NOT 42))')

process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
                                                      vertexCollection = cms.InputTag('offlinePrimaryVertices'),
                                                      minimumNDOF = cms.uint32(4) ,
                                                      maxAbsZ = cms.double(24),
                                                      maxd0 = cms.double(2)
                                                      )

process.phaseHF = cms.EDAnalyzer ("phiSym",
    textFile = cms.untracked.string('yhisto_6.txt'),
    gainFile = cms.untracked.string('gain_6.txt'),
    triggerResultsLabel = cms.InputTag("TriggerResults::HLT"),
    l1GtUnpack = cms.untracked.string('l1GtUnpack')
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('yhisto_6.root'),
)

# -------------------------  HBHEHF RECO

from EventFilter.HcalRawToDigi.HcalRawToDigi_cfi import *

from RecoLocalCalo.HcalRecProducers.HcalHitReconstructor_hbhe_cfi import *
#from RecoLocalCalo.HcalRecProducers.HcalHitReconstructor_ho_cfi import *
from RecoLocalCalo.HcalRecProducers.HcalHitReconstructor_hf_cfi import *
from RecoLocalCalo.HcalRecProducers.HBHEIsolatedNoiseReflagger_cfi import *
process.newhbheprereco = hbheprereco.clone()
#process.newhbhereco    = hbhereco.clone()
#process.newhoreco      = horeco.clone()
process.newhfreco      = hfreco.clone()
#process.newhbhereco.hbheInput    = "newhbheprereco"
process.newhcalLocalRecoSequence = cms.Sequence(process.newhbheprereco+process.newhfreco)
#process.newhcalLocalRecoSequence = cms.Sequence(process.newhbheprereco+process.newhbhereco+process.newhfreco+process.newhoreco)

#--------------------------- Making re-digi/re-reco and analysing
#process.hcalDigis.InputLabel = 'source' # data RAW input


process.p = cms.Path(
process.primaryVertexFilter*
 #process.hcalDigis *
# process.newhcalLocalRecoSequence *
 process.phaseHF
) 

process.source = cms.Source ("PoolSource" ,
fileNames=cms.untracked.vstring(
'/store/data/Run2012B/DoubleElectron/RAW-RECO/ZElectron-13Jul2012-v1/00000/023A7D47-C8D5-E111-AF13-003048678BAE.root'
#'/store/data/Run2012B/DoubleElectron/RAW/v1/000/195/930/7A3B6D92-87B2-E111-9F8D-001D09F291D7.root',
#'/store/data/Run2012B/DoubleElectron/RAW/v1/000/195/930/6C248C45-7BB2-E111-B34B-BCAEC518FF8E.root',
#'/store/data/Run2012B/DoubleElectron/RAW/v1/000/195/930/5AD5A8F2-94B2-E111-AE1E-5404A63886C1.root',
#'/store/data/Run2012B/DoubleElectron/RAW/v1/000/195/930/52670532-83B2-E111-95AE-BCAEC5364C4C.root'
)
)
import FWCore.PythonUtilities.LumiList as LumiList
#process.source.lumisToProcess = LumiList.LumiList(filename = 'Cert_190456-208686_8TeV_PromptReco_Collisions12_JSON.tx').getVLuminosityBlockRange()
 
