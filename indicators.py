import json

#两种分类，常用指标和全量指标
indicators = [{
   'label':'请选择',
   'value':0,
   'children':[{
      'label':'请选择',
      'value': 0
   }]
},{
   'label':'通用指标',
   'value':1,
   'children':[{
      'label':'加/减速指标(AC)',
      'value': 0
   },{
      'label':'MACD',
      'value': 1
   }]
},{
   'label':'全量指标',
   'value':2,
   'children':[{
      'label':'加/减速指标(AC)',
      'value': 0
   },{
      'label':'Accum',
      'value': 1
   },{
      'label':'AdaptiveMovingAverage',
      'value': 2
   },{
      'label':'AdaptiveMovingAverageEnvelope',
      'value': 3
   }]
}]

AccelerationDecelerationOscillator = {}
Accum = {}
AdaptiveMovingAverage = {}
AdaptiveMovingAverageEnvelope = {}
AdaptiveMovingAverageOscillator = {}
AllN = {}
AnyN = {}
ApplyN = {}
AroonDown = {}
AroonOscillator = {}
AroonUp = {}
AroonUpDown = {}
AroonUpDownOscillator = {}
Average = {}
AverageDirectionalMovementIndex = {}
AverageDirectionalMovementIndexRating = {}
AverageTrueRange = {}
AwesomeOscillator = {}
BaseApplyN = {}
BollingerBands = {}
BollingerBandsPct = {}
CointN = {}
CommodityChannelIndex = {}
CrossDown = {}
CrossOver = {}
CrossUp = {}
DV2 = {}
DemarkPivotPoint = {}
DetrendedPriceOscillator = {}
DicksonMovingAverage = {}
DicksonMovingAverageEnvelope = {}
DicksonMovingAverageOscillator = {}
DirectionalIndicator = {}
DirectionalMovement = {}
DirectionalMovementIndex = {}
DoubleExponentialMovingAverage = {}
DoubleExponentialMovingAverageEnvelope = {}
DoubleExponentialMovingAverageOscillator = {}
DownDay = {}
DownDayBool = {}
DownMove = {}
Envelope = {}
ExponentialMovingAverage = {}
ExponentialMovingAverageEnvelope = {}
ExponentialMovingAverageOscillator = {}
ExponentialSmoothing = {}
ExponentialSmoothingDynamic = {}
FibonacciPivotPoint = {}
FindFirstIndex = {}
FindFirstIndexHighest = {}
FindFirstIndexLowest = {}
FindLastIndex = {}
FindLastIndexHighest = {}
FindLastIndexLowest = {}
Fractal = {}
HeikinAshi = {}
Highest = {}
HullMovingAverage = {}
HullMovingAverageEnvelope = {}
HullMovingAverageOscillator = {}
HurstExponent = {}
Ichimoku = {}
KnowSureThing = {}
LaguerreFilter = {}
LaguerreRSI = {}
LinePlotterIndicator = {}
Lowest = {}
MACD = {}
MACDHisto = {}
MeanDeviation = {}
MinusDirectionalIndicator = {}
Momentum = {}
MomentumOscillator = {}
MovingAverageBase = {}
MovingAverageSimple = {}
MovingAverageSimpleEnvelope = {}
MovingAverageSimpleOscillator = {}
NonZeroDifference = {}
OLS_BetaN = {}
OLS_Slope_InterceptN = {}
OLS_TransformationN = {}
OperationN = {}
Oscillator = {}
OscillatorMixIn = {}
ParabolicSAR = {}
PercentChange = {}
PercentRank = {}
PercentagePriceOscillator = {}
PercentagePriceOscillatorShort = {}
PeriodN = {}
PivotPoint = {}
PlusDirectionalIndicator = {}
PrettyGoodOscillator = {}
PriceOscillator = {}
RSI_EMA = {}
RSI_SMA = {}
RSI_Safe = {}
RateOfChange = {}
RateOfChange100 = {}
ReduceN = {}
RelativeMomentumIndex = {}
RelativeStrengthIndex = {}
Signal = {}
SmoothedMovingAverage = {}
SmoothedMovingAverageEnvelope = {}
SmoothedMovingAverageOscillator = {}
StandardDeviation = {}
Stochastic = {}
StochasticFast = {}
StochasticFull = {}
SumN = {}
TripleExponentialMovingAverage = {}
TripleExponentialMovingAverageEnvelope = {}
TripleExponentialMovingAverageOscillator = {}
Trix = {}
TrixSignal = {}
TrueHigh = {}
TrueLow = {}
TrueRange = {}
TrueStrengthIndicator = {}
UltimateOscillator = {}
UpDay = {}
UpDayBool = {}
UpMove = {}
Vortex = {}
WeightedAverage = {}
WeightedMovingAverage = {}
WeightedMovingAverageEnvelope = {}
WeightedMovingAverageOscillator = {}
WilliamsAD = {}
WilliamsR = {}
ZeroLagExponentialMovingAverage = {}
ZeroLagExponentialMovingAverageEnvelope = {}
ZeroLagExponentialMovingAverageOscillator = {}
ZeroLagIndicator = {}
ZeroLagIndicatorEnvelope = {}
ZeroLagIndicatorOscillator = {}
haDelta = {}