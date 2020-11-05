#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tabula import read_pdf

if __name__ == "__main__":
    file = "test.pdf"
    data = read_pdf(file, pages = 49)
    print(data)

