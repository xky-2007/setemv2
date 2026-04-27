import os, json, datetime

base = r'C:\Users\xky\Desktop\seteam workspace\projects\event-planning-v2'
os.makedirs(base, exist_ok=True)
os.makedirs(f'{base}\\state', exist_ok=True)
os.makedirs(f'{base}\\shared\\discussions\\inner_circle', exist_ok=True)
os.makedirs(f'{base}\\shared\\outputs', exist_ok=True)

# Mission
mission = {
    'mission_id': 'mission_001',
    'created_at': '2026-04-27T12:54:00+08:00',
    'task': '为大学生社团策划一场完整的线下迎新活动方案',
    'requirements': '活动主题/流程安排/物料预算/人员分工/风险应急预案/宣传文案，要求可直接落地执行',
    'user': 'webchat',
    'status': 'initialized'
}
with open(f'{base}\\state\\00_mission.json', 'w', encoding='utf-8') as f:
    json.dump(mission, f, ensure_ascii=False, indent=2)
print('Mission initialized:', mission['mission_id'])

# Shared inputs
shared_inputs = {
    'task_type': 'event-planning',
    'domain': 'campus-organization',
    'target': 'college-freshmen-welcome-event',
    'constraints': ['offline', 'budget-conscious', 'executable'],
    'output_format': 'markdown'
}
with open(f'{base}\\shared\\inputs.json', 'w', encoding='utf-8') as f:
    json.dump(shared_inputs, f, ensure_ascii=False, indent=2)
print('Shared inputs created')
