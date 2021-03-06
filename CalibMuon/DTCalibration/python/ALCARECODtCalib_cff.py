import FWCore.ParameterSet.Config as cms

import copy
from HLTrigger.HLTfilters.hltHighLevel_cfi import *

from CalibMuon.DTCalibration.DTCalibMuonSelection_cfi import *

# AlCaReco for DT calibration
ALCARECODtCalibHLTFilter = copy.deepcopy(hltHighLevel)
#ALCARECODtCalibHLTFilter.andOr = True ## choose logical OR between Triggerbits
#ALCARECODtCalibHLTFilter.HLTPaths = ['HLT_L1MuOpen*', 'HLT_L1Mu*']
ALCARECODtCalibHLTFilter.throw = False ## dont throw on unknown path names
ALCARECODtCalibHLTFilter.eventSetupPathsKey = 'DtCalib'

import RecoLocalMuon.DTSegment.dt4DSegments_CombPatternReco4D_LinearDriftFromDB_cfi as dt4DSegmentsCfiRef
dt4DSegmentsNoWire = dt4DSegmentsCfiRef.dt4DSegments.clone()
dt4DSegmentsNoWire.Reco4DAlgoConfig.recAlgoConfig.tTrigModeConfig.doWirePropCorrection = False
dt4DSegmentsNoWire.Reco4DAlgoConfig.Reco2DAlgoConfig.recAlgoConfig.tTrigModeConfig.doWirePropCorrection = False

#this is to select collisions
from RecoMET.METFilters.metFilters_cff import primaryVertexFilter, noscraping

# Short-term workaround to preserve the "run for every event" while removing the use of convertToUnscheduled()
# To be reverted in a subsequent PR
seqALCARECODtCalibTask = cms.Task(dt4DSegmentsNoWire)
seqALCARECODtCalib = cms.Sequence(primaryVertexFilter * noscraping * ALCARECODtCalibHLTFilter * DTCalibMuonSelection, seqALCARECODtCalibTask)

## customizations for the pp_on_AA_2018 eras
from Configuration.Eras.Modifier_pp_on_AA_2018_cff import pp_on_AA_2018
pp_on_AA_2018.toModify(ALCARECODtCalibHLTFilter,
                       eventSetupPathsKey='DtCalibHI'
)

seqALCARECODtCalibHI = cms.Sequence(ALCARECODtCalibHLTFilter, seqALCARECODtCalibTask)

#Specify to use HI sequence for the pp_on_AA_2018 eras
pp_on_AA_2018.toReplaceWith(seqALCARECODtCalib,seqALCARECODtCalibHI)
