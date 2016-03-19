"""
This is a sample mean-reversion algorithm on Quantopian for you to test and adapt.
This example uses pipeline to set its universe daily.

Algorithm investment thesis: 
Top-performing stocks from last week will do worse this week, and vice-versa.

Every Monday, we rank high dollar volume stocks based on their previous 5 day returns. 
We long the bottom 10% of stocks with the WORST returns over the past 5 days.
We short the top 10% of stocks with the BEST returns over the past 5 days.


This type of algorithm may be used in live trading and in the Quantopian Open.
"""

# Import the libraries we will use here
from quantopian.algorithm import attach_pipeline, pipeline_output
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.factors import AverageDollarVolume, Returns

"""
The initialize function is the place to create your pipeline (stock selector),
and set trading conditions such as commission and slippage. It is called once
at the start of the simulation and also where context variables can be set.
"""
def initialize(context):
    
    # Define context variables that can be accessed in other methods of
    # the algorithm.
    context.long_leverage = 0.5
    context.short_leverage = -0.5
    context.returns_lookback = 5
           
    # Rebalance every Monday (or the first trading day if it's a holiday).
    # At 11AM ET, which is 1 hour and 30 minutes after market open.
    schedule_function(rebalance, 
                      date_rules.week_start(days_offset=0),
                      time_rules.market_open(hours = 1, minutes = 30))
    
    # Record tracking variables at the end of each day.
    schedule_function(record_vars,
                      date_rules.every_day(),
                      time_rules.market_close(minutes=1))
    
    # Create and attach our pipeline (dynamic stock selector), defined below.
    attach_pipeline(make_pipeline(context), 'mean_reversion_example')
        
"""
A function to create our pipeline (dynamic stock selector). The pipeline is used
to rank stocks based on different factors, including builtin facotrs, or custom 
factors that you can define. Documentation on pipeline can be found here:
    https://www.quantopian.com/help#pipeline-title
"""
def make_pipeline(context):
    
    # Create a pipeline object. 
    pipe = Pipeline()
    
    # Create a dollar_volume factor using default inputs and window_length.
    # This is a builtin factor.
    dollar_volume = AverageDollarVolume(window_length=1)
    pipe.add(dollar_volume, 'dollar_volume')
    
    # Create a recent_returns factor with a 5-day returns lookback. This is
    # a custom factor defined below (see RecentReturns class).
    recent_returns = Returns(window_length=context.returns_lookback)
    pipe.add(recent_returns, 'recent_returns')
    
    # Define high dollar-volume filter to be the top 5% of stocks by dollar volume.
    high_dollar_volume = dollar_volume.percentile_between(95, 100)
    
    # Define high and low returns filters to be the bottom 10% and top 10% of
    # securities in the high dollar volume group.
    low_returns = recent_returns.percentile_between(0,10,mask=high_dollar_volume)
    high_returns = recent_returns.percentile_between(90,100,mask=high_dollar_volume)
    
    # Factors return a scalar value for each security in the entire universe
    # of securities. Here, we add the recent_returns rank factor to our pipeline
    # and we provide it with a mask such that securities that do not pass the mask
    # (i.e. do not have high dollar volume), are not considered in the ranking.
    pipe.add(recent_returns.rank(mask=high_dollar_volume), 'recent_returns_rank')
    
    # Add a filter to the pipeline such that only high-return and low-return
    # securities are kept.
    pipe.set_screen((low_returns | high_returns) & high_dollar_volume)
    
    # Add the low_returns and high_returns filters as columns to the pipeline so
    # that when we refer to securities remaining in our pipeline later, we know
    # which ones belong to which category.
    pipe.add(low_returns, 'low_returns')
    pipe.add(high_returns, 'high_returns')
    
    return pipe

"""
Called every day before market open. This is where we get the securities
that made it through the pipeline.
"""
def before_trading_start(context, data):
    
    # Pipeline_output returns a pandas DataFrame with the results of our factors
    # and filters.
    context.output = pipeline_output('mean_reversion_example')
    
    # Sets the list of securities we want to long as the securities with a 'True'
    # value in the low_returns column.
    context.long_secs = context.output[context.output['low_returns']]
    
    # Sets the list of securities we want to short as the securities with a 'True'
    # value in the high_returns column.
    context.short_secs = context.output[context.output['high_returns']]
    
    # Update our universe to contain the securities that we would like to long and short.
    update_universe(context.long_secs.index.union(context.short_secs.index))

"""
This rebalancing function is called according to our schedule_function settings.  
"""
def rebalance(context,data):
    
    # Get any open orders that we may have, to prevent double ordering.
    open_orders = get_open_orders()
        
    # Set the allocations to even weights in each portfolio.
    long_weight = context.long_leverage / (len(context.long_secs) + len(open_orders)/2)
    short_weight = context.short_leverage / (len(context.short_secs) + len(open_orders)/2)
    
    # For each security in our universe, order long or short positions according
    # to our context.long_secs and context.short_secs lists, and sell all previously
    # held positions not in either list.
    for stock in data:
        # Guard against ordering too much of a given security if a previous order
        # is still unfilled.
        if stock not in open_orders:
            if stock in context.long_secs.index:
                order_target_percent(stock, long_weight)
            elif stock in context.short_secs.index:
                order_target_percent(stock, short_weight)
            else:
                order_target_percent(stock, 0)
    
    # Log the long and short orders each week.
    log.info("This week's longs: "+", ".join([long_.symbol for long_ in context.long_secs.index]))
    log.info("This week's shorts: "  +", ".join([short_.symbol for short_ in context.short_secs.index]))

"""
This function is called at the end of each day and plots certain variables.
"""
def record_vars(context, data):
    
    # Record and plot the leverage of our portfolio over time. Even in minute
    # mode, only the end-of-day leverage is plotted.
    record(leverage = context.account.leverage)

    # We also want to monitor the number of long and short positions 
    # in our portfolio over time. This loop will check our positition sizes 
    # and add the count of longs and shorts to our plot.
    longs = shorts = 0
    for position in context.portfolio.positions.itervalues():
        if position.amount > 0:
            longs += 1
        if position.amount < 0:
            shorts += 1
    record(long_count=longs, short_count=shorts)

"""
The handle_data function is called every minute. There is nothing that we want
to do every minute in this algorithm.
"""
def handle_data(context,data):
    pass
