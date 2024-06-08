import json
from data_inputer import DataInputer

from risk_assessor import RiskAssessor
from validator import Validator

if __name__ == '__main__':
    with open('./Alpha/common_columns.json') as f:
        common_columns = json.load(f)
    data_inputer = DataInputer(common_columns)
    
    risk_assessor = RiskAssessor(
        data_inputer=data_inputer,
        common_columns=common_columns,
        ds2_doctor_vote=3,
        ds4_doctor_vote=2
    )
    
    query = {
        'gender': 'Female',
        'race': 'African American',
        'smoking history': 'Currently smoking',
        'height - cm': 153,
        'weight - kg': 35,
        'age': 110,
        'urine': 12.1824
    }
    
    if query is None:
        validated_data = data_inputer.get_mock_data()
    else:
        validated_data = data_inputer.get_valid_input(query)
    
    risk = risk_assessor.calculate_risk(query=validated_data)
    print(f"Risk assessment: {risk}")
    
    validator = Validator(data_inputer, risk_assessor)
    validator.validate_ds2()
    validator.validate_ds4()
