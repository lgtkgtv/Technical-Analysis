# interactive_rsi_v2_final.py

import yfinance as yf
import pandas as pd
import sys      # Used for flushing print output
import os       # Used for clearing the terminal screen (optional)
import numpy as np # Essential for handling the division by zero edge case

# --- Helper Function for Interactivity ---
def wait_for_keystroke(message="Press ENTER to continue...") -> None:
    """Pauses the program until the user presses Enter."""
    print(f"\n{message}", end="")
    sys.stdout.flush() 
    input()
    print("-" * 50)

# --- Function 1: Data Acquisition ---
def fetch_stock_data(ticker: str, period: str) -> pd.DataFrame:
    """
    Downloads historical stock data using yfinance.
    :param ticker: The stock ticker symbol.
    :param period: The historical period to fetch.
    :return: A Pandas DataFrame containing OHLCV data.
    """
    # Clear the console for a clean step
    os.system('clear' if os.name == 'posix' else 'cls') 
    print(f"[FUNCTION: fetch_stock_data called with ticker='{ticker}', period='{period}']")
    print("We are using the **yfinance library** to connect to Yahoo Finance.")
    
    # yfinance code: Downloads the data. progress=False suppresses the download bar.
    stock_data = yf.download(ticker, period=period, progress=False)
    
    print("Code: stock_data = yf.download(ticker, period=period, progress=False)")
    
    if stock_data.empty:
        raise ValueError(f"Could not retrieve data for ticker {ticker}. Check the symbol.")
        
    print(f"Return Value: DataFrame with {len(stock_data)} rows.")
    
    print("\n✅ Raw Data Snapshot (Last 5 records):")
    # Pandas code: .tail() returns the last N rows. .to_markdown() formats it nicely.
    print(stock_data.tail().to_markdown(numalign="left", stralign="left"))
    return stock_data

# --- Function 2: RSI Calculation (Core Logic) ---
def calculate_rsi(data: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    Calculates the Relative Strength Index (RSI) in an interactive, step-by-step manner.
    :param data: Input DataFrame containing 'Close' prices.
    :param period: The look-back period for RSI (default 14).
    :return: The DataFrame with a new 'RSI' column added.
    """
    print(f"\n[FUNCTION: calculate_rsi called with period={period}]")
    wait_for_keystroke("Press ENTER to proceed to Step 3: Finding Daily Moves...")

    # --- Step 3: Daily Price Changes (Delta) ---
    print("\n[Step 3: Calculating Daily Moves (Delta)]")
    # Pandas code: .diff(1) calculates the difference between the current row and the previous row.
    delta = data['Close'].diff(1)
    print("Code: delta = data['Close'].diff(1)")
    
    # Separate Gains and Losses
    delta.dropna(inplace=True)
    gain = delta.copy()
    loss = delta.copy()
    
    # Pandas code: For 'gain', any negative value (loss) is set to 0.
    gain[gain < 0] = 0
    # Pandas code: For 'loss', any positive value (gain) is set to 0.
    loss[loss > 0] = 0
    wait_for_keystroke()
    
    # --- Step 4: Smoothing (Average Gains/Losses) ---
    print("\n[Step 4: Smoothing the Data (Exponential Moving Average)]")
    print(f"We average the gains/losses over the last {period} days. This removes short-term noise.")
    
    # Pandas code: .ewm(span=period) calculates the Exponentially Weighted Moving Average (EWMA).
    avg_gain = gain.ewm(span=period, min_periods=period).mean()
    avg_loss = loss.abs().ewm(span=period, min_periods=period).mean()
    
    # FIX: Use pd.concat for reliable index alignment and then drop NaNs
    # Pandas code: pd.concat combines the two Series into one DataFrame along the columns (axis=1).
    avg_comparison = pd.concat([avg_gain, avg_loss], axis=1)
    avg_comparison.columns = ['Average_Gain', 'Average_Loss']
    # Pandas code: .dropna(inplace=True) removes the initial 'period' (14) rows which are NaN.
    avg_comparison.dropna(inplace=True) 
    
    print("Code: avg_comparison = pd.concat(...).dropna()")
    print("Average Gain/Loss Snapshot (Last 3 records):")
    print(avg_comparison.tail(3).to_markdown(numalign="left", stralign="left"))
    wait_for_keystroke()

    # --- Step 5: Relative Strength (RS) Ratio (FINAL FIX) ---
    print("\n[Step 5: Calculating Relative Strength (RS) Ratio]")
    print("$$ \text{RS} = \\frac{\\text{Average Gain}}{\\text{Average Loss}} $$")
    
    # 1. Get the cleaned, aligned Series data
    aligned_gain = avg_gain.dropna()
    aligned_loss = avg_loss.dropna()
    
    # 2. Use np.where to handle division by zero (Average_Loss = 0). 
    # rs_values_array is the intermediate result, potentially a (N, 1) array.
    rs_values_array = np.where(aligned_loss.values == 0, 100.0, aligned_gain.values / aligned_loss.values)
    
    # 3. GUARANTEED FIX: Use .ravel() to ensure the array is strictly 1-dimensional (flat).
    rs_flat_values = rs_values_array.ravel()
    
    # 4. Convert the resulting flat numpy array back into a pandas Series with the correct index.
    rs = pd.Series(rs_flat_values, index=aligned_loss.index) 
    
    # Create verbose comparison table
    rs_comparison = avg_comparison.copy()
    rs_comparison['RS_Ratio'] = rs
    
    print("Code: rs = pd.Series(np.where(loss == 0, 100, gain/loss)).ravel()")
    print("RS Ratio Snapshot (Last 3 records):")
    print(rs_comparison.tail(3).to_markdown(numalign="left", stralign="left"))
    wait_for_keystroke()
    
    # --- Step 6: Final RSI Score ---
    print("\n[Step 6: Calculating the Final RSI Score (0-100)]")
    print("$$ \text{RSI} = 100 - \\left(\\frac{100}{1 + \\text{RS}}\\right) $$")
    
    # Pandas code: Applies the final formula to the RS series to get the RSI score.
    rsi = 100 - (100 / (1 + rs))
    
    # Final assignment: Uses the safe .loc accessor to insert the calculated RSI scores 
    data.loc[rsi.index, 'RSI'] = rsi
    
    print("Code: data.loc[rsi.index, 'RSI'] = rsi")
    print("Return Value: Original DataFrame with new 'RSI' column.")
    return data

# --- Function 3: Interpretation (Main Explanation) ---
def interpret_results(data: pd.DataFrame, ticker: str) -> None:
    """
    Interprets the final RSI value to provide a clear trading assessment.
    """
    print(f"\n[FUNCTION: interpret_results called for {ticker}]")
    wait_for_keystroke("Press ENTER to proceed to Step 7: Interpreting the Finding...")

    print("\n[Step 7: Interpreting the Finding]")
    
    # Pandas code: .iloc[-1] gets the very last (most recent) value in the series.
    last_rsi = data['RSI'].iloc[-1]
    
    print("Final Results Snapshot (Close Price and Final RSI):")
    print(data[['Close', 'RSI']].tail(3).to_markdown(numalign="left", stralign="left"))
    
    wait_for_keystroke()

    print(f"\nFinal Score: **{ticker}'s RSI is {last_rsi:.2f}**")
    print("-----------------------------------")
    
    # The nan check
    if np.isnan(last_rsi):
        print("🚨 **ERROR: RSI is NaN/Undetermined.** This happens if there are no price movements (no gain/loss) in the last 14 days.")
        print("We cannot determine a stress level. Try a different ticker or a longer period.")
    elif last_rsi > 70:
        print("🚨 **OVERBOUGHT (Score > 70):** The stock is too expensive. A drop (correction) is expected.")
        print("Analogy: The price balloon is inflated too high. This is a potential SELL signal.")
        print("")
    elif last_rsi < 30:
        print("🟢 **OVERSOLD (Score < 30):** The stock is too cheap. A bounce (reversal) is expected.")
        print("Analogy: The price spring is compressed too tight. This is a potential BUY signal.")
        print("")
    else:
        print("🟡 **NEUTRAL ZONE (30 to 70):** The market is balanced. We need other tools for signals.")
        
    print("\n--- TUTORIAL COMPLETE ---")

# --- Main Program Execution ---
if __name__ == '__main__':
    
    # Configuration
    TICKER = "NVDA"
    PERIOD = "1y"
    RSI_PERIOD = 14
    
    print("--- 🧠 RSI TUTORIAL: Stock Stress Monitor (V2 FINAL) ---")
    wait_for_keystroke("Press ENTER to begin the tutorial...")
    
    try:
        # 1. Data Acquisition
        stock_data = fetch_stock_data(TICKER, PERIOD)
        
        # 2. RSI Calculation
        df_with_rsi = calculate_rsi(stock_data, RSI_PERIOD)
        
        # 3. Interpretation
        interpret_results(df_with_rsi, TICKER)
        
    except ValueError as e:
        print(f"\n[FATAL ERROR]: {e}")
        print("The program terminated due to a data retrieval issue. Check your internet connection or ticker symbol.")
    except Exception as e:
        print(f"\n[FATAL ERROR]: An unexpected error occurred: {e}")
