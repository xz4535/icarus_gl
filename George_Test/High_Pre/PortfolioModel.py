from AlgorithmImports import *

class FixedDollarAmountPortfolioConstructionModel(PortfolioConstructionModel):
    '''Provides an implementation of IPortfolioConstructionModel that gives equal weighting to all securities.
    The target percent holdings of each security is 1/N where N is the number of securities.
    For insights of direction InsightDirection.UP, long targets are returned and
    for insights of direction InsightDirection.DOWN, short targets are returned.'''

    def __init__(self, rebalance = Resolution.DAILY, portfolio_bias = PortfolioBias.LONG_SHORT):
        '''Initialize a new instance of EqualWeightingPortfolioConstructionModel
        Args:
            rebalance: Rebalancing parameter. If it is a timedelta, date rules or Resolution, it will be converted into a function.
                              If None will be ignored.
                              The function returns the next expected rebalance time for a given algorithm UTC DateTime.
                              The function returns null if unknown, in which case the function will be called again in the
                              next loop. Returning current time will trigger rebalance.
            portfolio_bias: Specifies the bias of the portfolio (Short, Long/Short, Long)'''
        super().__init__()
        self.portfolio_bias = portfolio_bias

        # If the argument is an instance of Resolution or Timedelta
        # Redefine rebalancing_func
        rebalancing_func = rebalance
        if isinstance(rebalance, int):
            rebalance = Extensions.to_time_span(rebalance)
        if isinstance(rebalance, timedelta):
            rebalancing_func = lambda dt: dt + rebalance
        if rebalancing_func:
            self.set_rebalancing_func(rebalancing_func)

    def determine_target_percent(self, active_insights):
        '''Will determine the target percent for each insight
        Args:
            active_insights: The active insights to generate a target for'''
        result = {}

        # give equal weighting to each security
        count = sum(x.direction != InsightDirection.FLAT and self.respect_portfolio_bias(x) for x in active_insights)
        percent = 0.1
        for insight in active_insights:
            result[insight] = (insight.direction if self.respect_portfolio_bias(insight) else InsightDirection.FLAT) * percent
        return result

    def respect_portfolio_bias(self, insight):
        '''Method that will determine if a given insight respects the portfolio bias
        Args:
            insight: The insight to create a target for
        '''
        return self.portfolio_bias == PortfolioBias.LONG_SHORT or insight.direction == self.portfolio_bias