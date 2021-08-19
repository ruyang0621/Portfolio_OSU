//
//  CalculatorSplitAmount.swift
//  Tips Calculator
//
//  Created by Ru Yang on 8/19/21.
//

import Foundation

struct CalculatorSplitAmount {
    
    var splitAmount: Float = 0.00
    
    mutating func calculatorResult(amount: Float, tipPercentage: Float, splitNum: Float) {
        splitAmount = amount * (tipPercentage + 1) / splitNum
    }
    
    func getResult() -> String {
        let resultString = String(format: "%.2f", splitAmount)
        return resultString
    }
    
}
