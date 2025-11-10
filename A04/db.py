import sys
import os
import sqlite3
import csv
from typing import List, Tuple


class DatabaseImporter:
	"""Import semicolon-delimited CSV files into an SQLite database and answer a query.

	Usage (PowerShell):
		python db.py world\\country.csv world\\countrylanguage.csv world\\city.csv

	Only global variable allowed is the instance created in main.
	"""

	def __init__(self, argv: List[str]):
		# Command-line CSV file paths (excluding script name)
		self.csv_paths: List[str] = argv[1:]
		self.db_path: str = "db.sqlite"
		# Open connection immediately; create database file if missing
		self.conn: sqlite3.Connection = sqlite3.connect(self.db_path)
		self.conn.execute("PRAGMA foreign_keys = ON")

	# ------------- Orchestration -------------
	def run(self) -> None:
		try:
			# Import only when paths are provided; otherwise just query existing DB
			for path in self.csv_paths:
				self.import_csv(path)
			# After import (or existing database), answer the Spanish language question
			self.answer_spanish_language()
		finally:
			self.conn.close()

	# ------------- Table existence helpers -------------
	def table_exists(self, table_name: str) -> bool:
		cur = self.conn.execute(
			"SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table_name,)
		)
		return cur.fetchone() is not None

	def tables_exist(self, names: List[str]) -> bool:
		return all(self.table_exists(n) for n in names)

	# ------------- CSV Import Logic -------------
	def import_csv(self, path: str) -> None:
		"""Import a single CSV file: create table if missing and load rows.

		Table name derived from filename stem. All columns stored as TEXT for simplicity.
		"""
		table_name = os.path.splitext(os.path.basename(path))[0]
		if self.table_exists(table_name):
			return  # Skip re-import

		if not os.path.isfile(path):
			print(f"Warning: CSV file not found: {path}")
			return

		with open(path, "r", newline="", encoding="utf-8") as f:
			reader = csv.reader(f, delimiter=";", quotechar='"')
			try:
				headers = next(reader)
			except StopIteration:
				print(f"Warning: CSV file empty: {path}")
				return
			headers = [self._normalize_header(h) for h in headers]
			self.create_table(table_name, headers)
			self.create_indices_if_applicable(table_name, headers)
			rows = []
			for row in reader:
				if len(row) == 0:
					continue
				# Pad row if shorter than headers; trim if longer
				if len(row) < len(headers):
					row += [None] * (len(headers) - len(row))
				elif len(row) > len(headers):
					row = row[: len(headers)]
				# Convert "NULL" string to actual None
				cleaned = [None if (cell == "NULL" or cell == "") else cell for cell in row]
				rows.append(cleaned)
			self.insert_rows(table_name, headers, rows)

	def _normalize_header(self, header: str) -> str:
		"""Return a safe SQLite column name derived from CSV header."""
		h = header.strip().strip('"')
		# Keep it simple; quote identifiers in SQL to avoid most issues
		return h

	def create_table(self, table_name: str, columns: List[str]) -> None:
		col_defs = [f'"{c}" TEXT' for c in columns]
		ddl = f'CREATE TABLE "{table_name}" ({", ".join(col_defs)})'
		self.conn.execute(ddl)
		self.conn.commit()

	def create_indices_if_applicable(self, table_name: str, columns: List[str]) -> None:
		cur = self.conn.cursor()
		if table_name == "country":
			if "Code" in columns:
				cur.execute('CREATE INDEX IF NOT EXISTS idx_country_code ON "country"("Code")')
		elif table_name == "countrylanguage":
			# Useful for our query
			if "Language" in columns:
				cur.execute('CREATE INDEX IF NOT EXISTS idx_cl_language ON "countrylanguage"("Language")')
			if "CountryCode" in columns:
				cur.execute('CREATE INDEX IF NOT EXISTS idx_cl_countrycode ON "countrylanguage"("CountryCode")')
		# Commit only if any indices created
		self.conn.commit()

	def insert_rows(self, table_name: str, columns: List[str], rows: List[List[str]]) -> None:
		if not rows:
			return
		placeholders = ",".join(["?" for _ in columns])
		sql = f'INSERT INTO "{table_name}" ({", ".join([f"\"{c}\"" for c in columns])}) VALUES ({placeholders})'
		with self.conn:  # transaction
			self.conn.executemany(sql, rows)

	# ------------- Query Logic -------------
	def answer_spanish_language(self) -> None:
		"""Print the list of countries where Spanish is used (based on countrylanguage table)."""
		required = ["country", "countrylanguage"]
		if not self.tables_exist(required):
			print("Database does not contain required tables to answer the question.")
			return
		query = (
			"SELECT c.Name FROM countrylanguage cl "
			"JOIN country c ON c.Code = cl.CountryCode "
			"WHERE cl.Language = ? ORDER BY c.Name"
		)
		cur = self.conn.execute(query, ("Spanish",))
		names = [r[0] for r in cur.fetchall()]
		question = "In what countries is used the Spanish language? Provide their full names, sorted alphabetically."
		print(question)
		if names:
			print("Answer:")
			for n in names:
				print(n)
		else:
			print("Answer: <none found>")


def main():
	app = DatabaseImporter(sys.argv)
	app.run()


if __name__ == "__main__":  # Only global variable is 'app' inside main
	main()

