import pandas as pd
import xlwings as xw
from datetime import date


class DataTransformations:
    """
    Class for cleaning data and saving into Excel file
    """

    def __init__(self, data: dict) -> None:
        self.df = pd.DataFrame(data=data)
        self.today = date.today()

    def __convert_to_float(self, row) -> float:
        """
        Converts given string input into float data type
        """
        row = (
            row.replace(" zł", "").replace(",", ".").replace("od ", "").replace(" ", "")
        )
        return float(row)

    def __clean_data(self) -> None:
        """
        Converts data in 'Price' column into float data type
        """
        self.df["Price"] = self.df["Price"].apply(self.__convert_to_float)

    def load_to_excel(self) -> None:
        """
        Loads data into Excel file
        """
        self.file_path = rf"Output\\morele_{self.today}.xlsx"
        self.df.to_excel(self.file_path, sheet_name=f"morele_{self.today}", index=False)

    def save_data(self) -> None:
        """
        Saves Excel file into "Output" directory
        """
        print("saving data...")
        self.__clean_data()
        self.load_to_excel()
        self.__format_sheet()
        self.__save_workbook()
        print("data has been saved")

    def __add_hyperlink(self) -> None:
        """
        Formats Excel workbook:
        - Changes offer name into hyperlink
        - Removes helper columns
        """
        self.ws.range("A1").api.EntireColumn.Insert()
        last_row = self.ws.used_range.last_cell.row
        for row in range(2, last_row + 1):
            self.ws.range(f"A{row}").add_hyperlink(
                self.ws.range(f"D{row}").value, self.ws.range(f"B{row}").value
            )
        self.ws.range("A1").value = "Model"
        self.ws.range("B:B").delete()
        self.ws.range("C:C").delete()

    def __save_workbook(self) -> None:
        """
        Saves and closes edited workbook
        """
        self.wb.save()
        self.wb.close()

    def __format_sheet(self) -> None:
        """
        Function performing all transformation and formatting
        """
        app = xw.App(visible=False)
        self.wb = xw.Book(self.file_path)
        self.ws = self.wb.sheets[0]

        self.__add_hyperlink()

        headers_rng = self.ws.range("A1:B1")
        headers_rng.color = (0, 153, 204)
        headers_rng.font.size = 11
        headers_rng.font.color = "#FFFFFF"
        self.ws.range("A:B").font.name = "Calibri"
        self.ws.range("A:B").columns.autofit()

        price_range = self.ws.range("B2").expand("down")
        price_range.number_format = "# ##0,00 zł;-# ##0,00 zł"

        data_range = self.ws.range("A1").expand("table")
        table = self.ws.tables.add(
            source=data_range,
            name="PricingTable",
            has_headers=True,
            table_style_name="TableStyleMedium2",
        )
