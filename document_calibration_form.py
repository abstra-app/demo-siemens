import abstra.forms as af
import abstra.workflows as aw
import pandas as pd
import plotly.express as px

# Step 1: Input Customer Information
customer_id = af.read("Enter Customer ID:")
customer_name = af.read_dropdown("Select Customer Name:", options=["Alice", "Bob", "Charlie"]) # This can by dynamically filled, based on the previously inputted customer ID
customer_address = af.read("Enter Customer Address:") # This can also be dynamically filled based on the customer ID

# Step 2: Input Device Under Test (DUT) Information
dut_id = af.read("Enter DUT ID:")
dut_manufacturer = af.read_dropdown("Select DUT Manufacturer:", options=["Manufacturer A", "Manufacturer B", "Manufacturer C"])
dut_type = af.read("Enter DUT Type:")
dut_serial = af.read("Enter DUT Serial:")
dut_calibration_date = af.read_date("Enter DUT Calibration Date:")

# Step 3: Input Measurement Data
measurement_schema = af.ListItemSchema().read_number("Enter Reference Value").read_number("Enter DUT Value")

while True:
    measurements = af.read_list(measurement_schema, min=1, max=3)

    # Transform measurements into a DataFrame
    df = pd.DataFrame(measurements)
    df.columns = ['reference_value', 'dut_value']  # Rename columns for clarity

    # Step 4: Perform Calculations and Data Conversions
    df['error'] = df['dut_value'] - df['reference_value']

    # Step 5: Show Results
    af.display_pandas(df)
    fig = px.line(df, x='reference_value', y='dut_value', title='DUT vs Reference')
    af.display_plotly(fig)

    # Step 6: Correct Results if Necessary
    corrected = af.read_multiple_choice("Correct results?", options=["Yes", "No"])
    if "No" in corrected:
        break

# Step 7: Save Results to Be Processed in Following Stage
aw.set_data("customer_id", customer_id)
aw.set_data("customer_name", customer_name)
aw.set_data("customer_address", customer_address)
aw.set_data("dut_id", dut_id)
aw.set_data("dut_manufacturer", dut_manufacturer)
aw.set_data("dut_type", dut_type)
aw.set_data("dut_serial", dut_serial)
aw.set_data("dut_calibration_date", dut_calibration_date)
aw.set_data("measurements", df.to_json(orient='records', lines=True))

af.display("Results saved successfully!")