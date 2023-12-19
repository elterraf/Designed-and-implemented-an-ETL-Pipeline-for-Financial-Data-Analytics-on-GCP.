create or replace  view `dataflow-stockdata.dataflow_stockdata_dataset.view_equity_insights`
as
SELECT
  *,
  -- Market sentiment: The relationship between the open and close prices can provide insights into market sentiment.
  CASE
    WHEN close_price > open_price THEN 'Positive Market Sentiment'
    WHEN close_price < open_price THEN 'Negative Market Sentiment'
  ELSE
  'Neutral Market Sentiment'
END
  AS market_sentiment,
  -- Price gaps: Price gaps occur when the close price of one trading day is different from the open price of the following trading day.
 --  LAG(close_price) OVER (PARTITION BY symbol ORDER BY date) AS gap,
  CASE
    WHEN open_price > LAG(close_price) OVER (PARTITION BY symbol ORDER BY date) THEN 'Gap Up'
    WHEN open_price < LAG(close_price) OVER (PARTITION BY symbol ORDER BY date) THEN 'Gap Down'
  ELSE
  'No Gap'
END
  AS price_gap,
  -- Trend identification: Analyzing the high and low prices over multiple trading periods can help identify trends in the stock's price movement.
  CASE
    WHEN low_price < LAG(low_price) OVER (PARTITION BY symbol ORDER BY date) AND high_price < LAG(high_price) OVER (PARTITION BY symbol ORDER BY date) THEN 'Downward Trend'
    WHEN low_price > LAG(low_price) OVER (PARTITION BY symbol ORDER BY date)
  AND high_price > LAG(high_price) OVER (PARTITION BY symbol ORDER BY date) THEN 'Upward Trend'
  ELSE
  'No Clear Trend'
END
  AS trend,
  -- Price patterns: The high and low prices can contribute to the identification of various price patterns, such as double tops, double bottoms, head and shoulders patterns, and triangles.
  CASE
    WHEN high_price = low_price THEN 'Consolidation'
    WHEN high_price > LAG(high_price) OVER (PARTITION BY Symbol ORDER BY date)
  AND low_price > LAG(low_price) OVER (PARTITION BY Symbol ORDER BY date) THEN 'Uptrend Continuation'
    WHEN high_price < LAG(high_price) OVER (PARTITION BY Symbol ORDER BY date) AND low_price < LAG(low_price) OVER (PARTITION BY Symbol ORDER BY date) THEN 'Downtrend Continuation'
  ELSE
  'No Clear Pattern'
END
  AS price_pattern,
  -- Stop loss and take profit levels: Traders often use the high and low prices to set stop loss and take profit levels.
  low_price * 0.95 AS stop_loss_level,
  high_price * 1.05 AS take_profit_level,
  -- "WAP" stands for Weighted Average Price. The Weighted Average Price represents the average price at which a stock has traded during a specific trading session.
  ROUND(total_turnover / no_of_shares,12) AS WAP,
  -- "Deliverable Quantity" refers to the number of shares that were actually delivered or transferred between buyers and sellers during a particular trading period.
  ROUND((Deliverable_quantity / no_of_shares) * 100,2) AS Percentage_Deli_Qty_to_Traded_Qty,
  --  Spread_High_Low and Spread_Close_Open provide information about the price movement and volatility of a stock.
  ROUND(high_price - low_price,2) AS spread_high_low,
  ROUND(close_price - open_price,2) AS spread_close_open
FROM (
  SELECT
    DISTINCT * except(id)
  FROM
    `dataflow-stockdata.dataflow_stockdata_dataset.financial_data`) a
    --WHERE symbol = 'Adani Ports'
ORDER BY
  date