import os, json, time
from datetime import datetime

BASE = r'C:\Users\xky\Desktop\seteam workspace'
MISSION = 'mission-001'
PROJECT = os.path.join(BASE, 'projects', MISSION)

os.makedirs(os.path.join(PROJECT, 'state'), exist_ok=True)
DISC = os.path.join(PROJECT, 'shared', 'discussions')
os.makedirs(DISC, exist_ok=True)

def now():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

def wj(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)

def dm(frm, to_a, topic, dtype, message):
    tid = 'disc_' + frm + '_' + str(int(time.time()))
    return {'id': tid, 'from': frm, 'to': to_a, 'topic': topic, 'type': dtype, 'message': message, 'timestamp': now(), 'status': 'open'}

print('='*60)
print('Pipeline Test: 个人作品集页面')
print('='*60)

# 01 clarifier
print('\n[Step 1] requirement_clarifier')
d1 = dm('requirement_clarifier', 'requirement_analyzer', '需求模糊讨论', 'question', '用户说要有动画要好看，confidence只有0.65，要继续吗？')
with open(os.path.join(DISC, 'disc_001.json'), 'w', encoding='utf-8') as f:
    json.dump(d1, f, ensure_ascii=False, indent=2)
wj(os.path.join(PROJECT, 'state', '01_clarified.json'), {'status': 'clarified', 'confidence': 0.65, 'completed_at': now()})
print('  [DISC] clarifier -> analyzer: 需求模糊，confidence=0.65')

# 02 analyzer
print('\n[Step 2] requirement_analyzer')
d2 = dm('requirement_analyzer', 'requirement_clarifier', '同意继续', 'agreement', 'confidence 0.65可以继续，用GSAP动画+Awwwards风格作为默认值')
with open(os.path.join(DISC, 'disc_002.json'), 'w', encoding='utf-8') as f:
    json.dump(d2, f, ensure_ascii=False, indent=2)
wj(os.path.join(PROJECT, 'state', '02_analyzed.json'), {'status': 'analyzed', 'complexity': 'medium', 'completed_at': now()})
print('  [DISC] analyzer -> clarifier: 同意继续，GSAP+Awwwards默认值')

# 03 matcher
print('\n[Step 3] experience_matcher')
d3 = dm('experience_matcher', 'planner', '历史经验可借鉴', 'suggestion', 'jxnu-enrollment-v5项目有完整设计系统，可复用GSAP动画+玻璃态卡片参数')
with open(os.path.join(DISC, 'disc_003.json'), 'w', encoding='utf-8') as f:
    json.dump(d3, f, ensure_ascii=False, indent=2)
wj(os.path.join(PROJECT, 'state', '03_matched.json'), {'status': 'matched', 'match_rate': 0.72, 'reference': 'jxnu-enrollment-v5', 'completed_at': now()})
print('  [DISC] matcher -> planner: 建议复用jxnu设计系统')

# 04 planner
print('\n[Step 4] planner')
d4 = dm('planner', 'experience_matcher', '收到借鉴建议', 'agreement', '同意复用jxnu设计系统，但需调整配色为个人风格')
with open(os.path.join(DISC, 'disc_004.json'), 'w', encoding='utf-8') as f:
    json.dump(d4, f, ensure_ascii=False, indent=2)
d5 = dm('planner', 'designer', '团队规模确认', 'question', 'P1有3个任务并行，Builder要几个？')
with open(os.path.join(DISC, 'disc_005.json'), 'w', encoding='utf-8') as f:
    json.dump(d5, f, ensure_ascii=False, indent=2)
wj(os.path.join(PROJECT, 'state', '04_planned.json'), {'status': 'planned', 'phases': 3, 'hours': 8, 'completed_at': now()})
print('  [DISC] planner -> matcher: 同意复用，调整配色')
print('  [DISC] planner -> designer: 询问Builder数量')

# 05 designer 讨论阶段
print('\n[Step 5] designer -- 讨论阶段启动')
d6 = dm('designer', 'all', '技术方案', 'question', '单页HTML+GSAP+CSS变量，轻量方案。其他人怎么看？')
with open(os.path.join(DISC, 'disc_006.json'), 'w', encoding='utf-8') as f:
    json.dump(d6, f, ensure_ascii=False, indent=2)
d7 = dm('requirement_analyzer', 'designer', 'SEO需求', 'suggestion', '同意轻量方案，但需要加meta description做SEO')
with open(os.path.join(DISC, 'disc_007.json'), 'w', encoding='utf-8') as f:
    json.dump(d7, f, ensure_ascii=False, indent=2)
d8 = dm('requirement_clarifier', 'designer', '鼠标光效建议', 'suggestion', '用户说好看，建议加鼠标跟随光效，Awwwards常见')
with open(os.path.join(DISC, 'disc_008.json'), 'w', encoding='utf-8') as f:
    json.dump(d8, f, ensure_ascii=False, indent=2)

disc_files = [f for f in os.listdir(DISC) if f.endswith('.json')]
print('  收到 ' + str(len(disc_files)) + ' 条讨论消息')

wj(os.path.join(PROJECT, 'state', '05_designed.json'), {
    'status': 'designed',
    'discussion_triggered': True,
    'discussion_summary': {
        'rounds': 1,
        'decisions': ['单页HTML+GSAP', '加meta description', '加鼠标跟随光效']
    },
    'team': {'roles': [{'id': 'builder'}, {'id': 'reviewer'}]},
    'completed_at': now()
})

with open(os.path.join(DISC, 'round_1_summary.md'), 'w', encoding='utf-8') as f:
    f.write('# 第1轮讨论收敛\n\n')
    f.write('## 共识结论\n')
    f.write('1. 技术方案：单页HTML+GSAP+CSS变量\n')
    f.write('2. SEO：添加meta description\n')
    f.write('3. 视觉亮点：加入鼠标跟随光效\n')
    f.write('\n## 参与Agent\n')
    for fname in sorted(disc_files):
        with open(os.path.join(DISC, fname), 'r', encoding='utf-8') as rf:
            d = json.load(rf)
            f.write('- ' + d['from'] + ': [' + d['type'] + '] ' + d['topic'] + '\n')
print('  讨论收敛，结论写入 round_1_summary.md')

print('\n' + '='*60)
print('Pipeline Test 完成！')
print('讨论消息: ' + str(len(disc_files)) + ' 条')
print('状态文件: 5 个 (01~05)')
print('讨论轮次: 1 轮收敛')
print()
print('--- 讨论消息 ---')
for fname in sorted(os.listdir(DISC)):
    if fname.endswith('.json'):
        with open(os.path.join(DISC, fname), 'r', encoding='utf-8') as f:
            d = json.load(f)
            print('  [' + d['type'].ljust(12) + '] ' + d['from'].ljust(25) + ' -> ' + d['to'].ljust(25) + ': ' + d['topic'])
print()
print('--- 状态文件 ---')
for fname in sorted(os.listdir(os.path.join(PROJECT, 'state'))):
    print('  ' + fname)
