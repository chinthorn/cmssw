import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('ntuple',eras.Phase2C2)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2023D4Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2023D4_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('Configuration.StandardSequences.VtxSmearedNoSmear_cff')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('L1Trigger.L1THGCal.hgcalTriggerPrimitives_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
    )

# Input source
process.source = cms.Source("PoolSource",
    secondaryFileNames = cms.untracked.vstring(),
#    fileNames = cms.untracked.vstring(
#        'file:./testGenOnly.root'
#        )
    fileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/user/lmastrol/UsrProd_Crab3/PhotonGunPt_15_150_900_pre4_Feb17_l1tpg/170222_134949/0000/l1tpg_gsdr_1.root')
)

# Additional output definition
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string("ntuple.root")
    )

# Path and EndPath definitions
process.digitisation_step = cms.Path(process.pdigi_valid)
process.L1simulation_step = cms.Path(process.SimL1Emulator)

# Remove best choice selection
process.hgcalTriggerPrimitiveDigiProducer.FECodec.NData = cms.uint32(999)
process.hgcalTriggerPrimitiveDigiProducer.FECodec.DataLength = cms.uint32(8)
process.hgcalTriggerPrimitiveDigiProducer.FECodec.triggerCellTruncationBits = cms.uint32(7)

process.hgcalTriggerPrimitiveDigiProducer.BEConfiguration.algorithms[0].calib_parameters.cellLSB = cms.double(
        process.hgcalTriggerPrimitiveDigiProducer.FECodec.linLSB.value() * 
        2 ** process.hgcalTriggerPrimitiveDigiProducer.FECodec.triggerCellTruncationBits.value() 
)


trgCells_algo_all =  cms.PSet( AlgorithmName = cms.string('SingleCellClusterAlgoBestChoice'),
                               FECodec = process.hgcalTriggerPrimitiveDigiProducer.FECodec,
                               HGCalEESensitive_tag = cms.string('HGCalEESensitive'),
                               HGCalHESiliconSensitive_tag = cms.string('HGCalHESiliconSensitive'),
                               calib_parameters = process.hgcalTriggerPrimitiveDigiProducer.BEConfiguration.algorithms[0].calib_parameters
                              )
cluster_algo_all =  cms.PSet( AlgorithmName = cms.string('HGCClusterAlgoBestChoice'),
                              FECodec = process.hgcalTriggerPrimitiveDigiProducer.FECodec,
                              HGCalEESensitive_tag = cms.string('HGCalEESensitive'),
                              HGCalHESiliconSensitive_tag = cms.string('HGCalHESiliconSensitive'),                           
                              calib_parameters = process.hgcalTriggerPrimitiveDigiProducer.BEConfiguration.algorithms[0].calib_parameters,
                              C2d_parameters = process.hgcalTriggerPrimitiveDigiProducer.BEConfiguration.algorithms[0].C2d_parameters,
                              C3d_parameters = process.hgcalTriggerPrimitiveDigiProducer.BEConfiguration.algorithms[0].C3d_parameters
                              )

process.hgcalTriggerPrimitiveDigiProducer.BEConfiguration.algorithms = cms.VPSet( cluster_algo_all )
process.hgcl1tpg_step = cms.Path( process.hgcalTriggerPrimitives ) 
process.digi2raw_step = cms.Path( process.DigiToRaw )
#process.HGC_clustering = cms.EDAnalyzer("testHGCClustering",
#                                        clusterInputTag=cms.InputTag("hgcalTriggerPrimitiveDigiProducer:HGCClusterAlgoBestChoice")
#                                        )

#process.test_step = cms.Path(process.HGC_clustering)

process.endjob_step = cms.EndPath(process.endOfProcess)

# load ntuplizer
process.load('L1Trigger.L1THGCal.hgcalTriggerNtuples_cff')
process.ntuple_step = cms.Path(process.hgcalTriggerNtuples) 
                                   
# Schedule definition
process.schedule = cms.Schedule( process.hgcl1tpg_step, 
                                 #process.digi2raw_step, 
                                 #process.test_step, 
                                 process.ntuple_step, # create the persistent event 
                                 process.endjob_step
                                 )

# filter all path with the production filter sequence
for path in process.paths:
        getattr(process,path)._seq

