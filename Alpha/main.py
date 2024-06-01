from risk_assessor import RiskAssessor

if __name__ == '__main__':
    
    medical_data = {
        'gender': 'Female',
        'race': 'African American',
        'smoking history': 'Currently smoking',
        'height - cm': 153,
        'weight - kg': 35,
        'age': 110,
        'urine': 12.1824
    }
    
    risk_assessor = RiskAssessor(ds2_doctor_vote=3, ds4_doctor_vote=2)
    risk = risk_assessor.calculate_risk(query=medical_data)
    print(f"Risk assessment: {risk}")
