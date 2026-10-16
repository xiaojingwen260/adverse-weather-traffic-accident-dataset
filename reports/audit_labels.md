# v1.0 最终验收审计 · 标签一致性 / 预测资格 / 划分 / 分布 / 元数据

审计时间：2026-10-05 14:35:25

## 1. 字段合法性与标签一致性

发现问题：**1500** 条

按严重程度：{'B': 1500}

| sample_id | 字段 | 值 | 问题 | 严重程度 |
|---|---|---|---|---|
| crash_day_normal_000001 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000002 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000003 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000004 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000005 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000006 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000007 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000008 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000009 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_rainy_000010 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000011 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000012 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000013 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000014 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000015 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000016 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000017 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000018 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000019 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000020 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000021 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000022 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000023 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000024 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000025 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000026 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000027 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000028 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000029 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000030 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000031 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000032 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000033 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_000034 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000035 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000036 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000037 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000038 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000039 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000040 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000041 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000042 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000043 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000044 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000045 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_000046 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000047 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000048 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000049 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_rainy_000050 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000051 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_000052 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000053 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000054 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000055 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000056 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000057 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000058 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000059 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000060 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000061 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000062 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000063 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000064 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000065 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000066 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000067 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000068 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000069 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000070 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000071 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000072 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000073 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000074 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000075 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000076 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000077 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000078 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000079 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000080 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000081 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000082 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000083 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000084 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000085 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_000086 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000087 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000088 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000089 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000090 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000091 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000092 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000093 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000094 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000095 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000096 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000097 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000098 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000099 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000100 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000101 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000102 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000103 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000104 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000105 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000106 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000107 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000108 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000109 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000110 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000111 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000112 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000113 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000114 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000115 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000116 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000117 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000118 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000119 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000120 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000121 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000122 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000123 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000124 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000125 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000126 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000127 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000128 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000129 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000130 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000131 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000132 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000133 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000134 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000135 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000136 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000137 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000138 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_rainy_000139 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000140 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000141 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000142 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000143 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000144 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000145 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000146 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000147 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000148 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000149 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000150 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000151 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000152 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000153 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000154 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000155 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000156 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000157 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000158 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000159 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000160 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000161 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000162 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000163 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000164 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000165 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000166 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000167 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000168 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000169 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000170 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000171 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000172 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000173 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000174 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000175 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000176 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000177 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000178 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000179 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000180 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000181 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000182 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000183 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000184 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000185 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000186 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000187 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000188 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000189 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000190 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000191 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000192 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000193 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000194 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000195 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000196 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000197 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000198 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000199 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000200 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000201 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000202 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000203 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000204 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000205 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000206 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000207 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000208 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000209 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000210 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000211 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_rainy_000212 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000213 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000214 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000215 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000216 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000217 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000218 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000219 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000220 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_000221 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000222 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000223 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000224 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000225 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000226 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000227 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000228 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000229 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000230 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000231 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000232 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000233 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000234 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000235 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000236 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000237 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000238 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000239 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000240 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000241 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000242 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000243 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000244 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000245 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000246 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000247 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000248 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000249 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000250 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000251 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000252 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000253 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000254 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000255 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000256 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000257 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000258 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000259 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000260 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000261 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000262 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000263 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000264 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000265 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000266 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000267 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000268 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000269 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000270 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000271 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000272 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000273 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000274 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000275 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000276 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000277 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000278 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000279 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000280 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000281 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000282 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000283 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000284 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000285 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000286 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000287 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000288 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000289 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000290 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000291 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000292 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000293 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000294 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000295 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000296 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000297 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000298 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000299 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000300 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000301 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000302 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000303 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000304 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000305 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000306 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000307 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000308 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000309 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000310 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000311 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000312 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000313 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000314 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000315 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000316 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000317 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000318 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000319 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000320 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000321 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000322 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000323 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000324 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000325 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000326 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000327 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000328 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000329 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000330 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000331 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000332 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000333 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000334 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000335 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000336 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000337 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000338 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000339 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000340 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000341 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000342 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000343 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000344 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000345 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000346 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000347 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000348 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000349 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000350 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000351 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000352 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000353 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000354 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000355 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000356 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_rainy_000357 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000358 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000359 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000360 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000361 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000362 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000363 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000364 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000365 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000366 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000367 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000368 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000369 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000370 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000371 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000372 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000373 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000374 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000375 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000376 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000377 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000378 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000379 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000380 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000381 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000382 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000383 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000384 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000385 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000386 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000387 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_000388 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000389 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000390 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000391 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000392 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000393 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000394 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_000395 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000396 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000397 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000398 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000399 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000400 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_000401 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000402 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000403 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000404 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000405 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000406 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000407 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000408 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000409 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000410 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000411 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000412 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000413 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000414 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000415 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000416 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000417 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000418 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000419 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000420 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000421 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000422 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000423 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000424 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000425 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000426 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000427 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000428 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000429 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000430 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000431 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000432 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000433 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000434 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000435 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000436 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000437 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000438 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000439 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000440 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000441 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000442 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000443 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000444 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000445 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000446 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_rainy_000447 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000448 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000449 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000450 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000451 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000452 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000453 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000454 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000455 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000456 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000457 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000458 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000459 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000460 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000461 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000462 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000463 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000464 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000465 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000466 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000467 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000468 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000469 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000470 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000471 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000472 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000473 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000474 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000475 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000476 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000477 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000478 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000479 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000480 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000481 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000482 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000483 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000484 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000485 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000486 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000487 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000488 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000489 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000490 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000491 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_rainy_000492 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000493 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000494 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000495 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000496 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000497 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000498 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000499 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000500 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000501 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000502 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000503 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_rainy_000504 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000505 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000506 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000507 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_000508 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_000509 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000510 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000511 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_000512 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000513 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000514 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000515 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000516 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000517 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000518 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000519 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000520 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000521 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000522 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000523 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000524 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000525 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_000526 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000527 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000528 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000529 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000530 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_000531 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000532 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000533 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000534 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000535 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_rainy_000536 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_rainy_000537 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000538 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000539 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000540 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000541 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000542 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000543 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000544 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000545 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000546 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000547 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000548 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000549 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000550 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000551 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000552 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_rainy_000553 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000554 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000555 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000556 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000557 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000558 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000559 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000560 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000561 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000562 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000563 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000564 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000565 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000566 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000567 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000568 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000569 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000570 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000571 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000572 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000573 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000574 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000575 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000576 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000577 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000578 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000579 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000580 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000581 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000582 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000583 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000584 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000585 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000586 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000587 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000588 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000589 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000590 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000591 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000592 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000593 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000594 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000595 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000596 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000597 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000598 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000599 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000600 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000601 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000602 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000603 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000604 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000605 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000606 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000607 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000608 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000609 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000610 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000611 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000612 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000613 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000614 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000615 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000616 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000617 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000618 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_000619 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000620 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000621 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000622 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000623 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000624 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000625 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000626 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000627 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000628 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000629 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000630 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000631 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000632 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000633 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000634 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000635 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000636 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000637 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000638 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000639 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000640 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000641 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000642 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000643 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000644 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000645 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000646 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000647 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000648 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_000649 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_000650 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000651 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000652 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_000653 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000654 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000655 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000656 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000657 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000658 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000659 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000660 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000661 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000662 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000663 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000664 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000665 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000666 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000667 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000668 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000669 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000670 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000671 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000672 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000673 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_rainy_000674 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000675 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000676 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000677 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000678 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000679 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000680 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000681 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000682 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000683 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000684 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000685 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000686 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000687 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000688 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000689 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000690 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000691 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000692 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000693 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000694 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000695 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_rainy_000696 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000697 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000698 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000699 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000700 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_rainy_000701 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000702 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000703 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000704 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000705 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000706 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000707 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000708 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000709 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000710 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000711 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000712 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000713 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000714 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000715 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000716 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000717 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000718 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000719 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000720 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000721 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000722 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000723 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000724 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000725 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000726 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000727 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000728 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000729 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000730 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000731 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000732 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000733 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000734 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000735 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000736 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000737 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000738 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_rainy_000739 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000740 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000741 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000742 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000743 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000744 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000745 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000746 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000747 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000748 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000749 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000750 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000751 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000752 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000753 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000754 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000755 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000756 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000757 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000758 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000759 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000760 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000761 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000762 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000763 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000764 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000765 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000766 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000767 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000768 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000769 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000770 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000771 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000772 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000773 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000774 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000775 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000776 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000777 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000778 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000779 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000780 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000781 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000782 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000783 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000784 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000785 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000786 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000787 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000788 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000789 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000790 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000791 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000792 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000793 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000794 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000795 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000796 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000797 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000798 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000799 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000800 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000801 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000802 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000803 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000804 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000805 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000806 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000807 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000808 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000809 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000810 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000811 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000812 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000813 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000814 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000815 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000816 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000817 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000818 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000819 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000820 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000821 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000822 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000823 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000824 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000825 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000826 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000827 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000828 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000829 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000830 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000831 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000832 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000833 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000834 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000835 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000836 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000837 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000838 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000839 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000840 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000841 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000842 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000843 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000844 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000845 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000846 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000847 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000848 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000849 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000850 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000851 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000852 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000853 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000854 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000855 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000856 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000857 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000858 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000859 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000860 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000861 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000862 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000863 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000864 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000865 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000866 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000867 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000868 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000869 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000870 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000871 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000872 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000873 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000874 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000875 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000876 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000877 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000878 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000879 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000880 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000881 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000882 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000883 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000884 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000885 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000886 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000887 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000888 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000889 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000890 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000891 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000892 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000893 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000894 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000895 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000896 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000897 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000898 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000899 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000900 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000901 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000902 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000903 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000904 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000905 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000906 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000907 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000908 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000909 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000910 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000911 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000912 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000913 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000914 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000915 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000916 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000917 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000918 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000919 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000920 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000921 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000922 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000923 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000924 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000925 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000926 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000927 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000928 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000929 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000930 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_000931 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000932 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000933 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000934 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000935 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000936 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000937 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000938 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000939 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000940 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000941 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000942 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000943 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000944 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000945 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000946 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000947 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000948 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000949 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000950 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000951 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000952 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000953 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000954 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000955 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000956 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000957 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000958 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000959 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000960 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000961 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000962 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000963 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000964 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000965 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000966 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000967 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000968 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000969 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000970 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000971 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000972 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000973 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000974 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000975 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000976 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000977 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000978 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000979 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000980 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000981 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000982 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000983 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000984 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000985 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000986 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000987 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000988 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000989 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_000990 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_000991 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000992 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000993 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000994 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000995 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000996 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000997 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_000998 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_000999 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001000 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001001 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001002 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001003 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001004 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001005 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001006 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001007 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001008 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001009 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001010 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001011 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001012 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001013 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_001014 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001015 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001016 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001017 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001018 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001019 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001020 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001021 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001022 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001023 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001024 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001025 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001026 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001027 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_001028 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001029 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001030 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001031 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001032 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001033 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001034 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001035 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001036 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001037 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001038 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001039 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001040 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001041 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001042 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001043 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001044 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001045 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001046 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001047 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001048 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001049 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001050 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001051 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001052 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001053 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001054 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001055 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001056 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001057 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001058 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001059 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001060 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001061 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001062 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001063 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001064 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001065 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001066 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001067 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001068 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001069 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001070 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001071 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001072 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001073 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001074 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001075 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001076 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001077 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001078 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001079 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001080 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001081 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001082 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001083 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001084 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001085 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001086 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001087 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001088 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001089 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001090 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001091 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001092 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001093 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001094 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001095 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001096 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001097 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001098 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001099 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_rainy_001100 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001101 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001102 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001103 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001104 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001105 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001106 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001107 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001108 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001109 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_001110 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001111 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001112 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_001113 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001114 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001115 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001116 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001117 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001118 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001119 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001120 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001121 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001122 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001123 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001124 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001125 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001126 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001127 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001128 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001129 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_001130 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001131 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001132 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001133 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001134 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001135 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001136 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_001137 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001138 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001139 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001140 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001141 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001142 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001143 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001144 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001145 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001146 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001147 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001148 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001149 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001150 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001151 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001152 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001153 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001154 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001155 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001156 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001157 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001158 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001159 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001160 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001161 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001162 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001163 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001164 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001165 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001166 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_001167 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001168 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001169 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001170 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001171 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001172 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001173 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001174 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001175 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_001176 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001177 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001178 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001179 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001180 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001181 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001182 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001183 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001184 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001185 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001186 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001187 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001188 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001189 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001190 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001191 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001192 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001193 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001194 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001195 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001196 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001197 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001198 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001199 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001200 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001201 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001202 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001203 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001204 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001205 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001206 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001207 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001208 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001209 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001210 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001211 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001212 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001213 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001214 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001215 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001216 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001217 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001218 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001219 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001220 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001221 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001222 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001223 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001224 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001225 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001226 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001227 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001228 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001229 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001230 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001231 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001232 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001233 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001234 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001235 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001236 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001237 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001238 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001239 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001240 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001241 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001242 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001243 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001244 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001245 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001246 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001247 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001248 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001249 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001250 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001251 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001252 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001253 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001254 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001255 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001256 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001257 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001258 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001259 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001260 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001261 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001262 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001263 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001264 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001265 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001266 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001267 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001268 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001269 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001270 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001271 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001272 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001273 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001274 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001275 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001276 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001277 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001278 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001279 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001280 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001281 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001282 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001283 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001284 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001285 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001286 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001287 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001288 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001289 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001290 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001291 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001292 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001293 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001294 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001295 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001296 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001297 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001298 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001299 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001300 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001301 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001302 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001303 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001304 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001305 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001306 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001307 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001308 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001309 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001310 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001311 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001312 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001313 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001314 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001315 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001316 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001317 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001318 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001319 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001320 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001321 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001322 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001323 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001324 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001325 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001326 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001327 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001328 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001329 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001330 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001331 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001332 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001333 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001334 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001335 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001336 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001337 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001338 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001339 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001340 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001341 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001342 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001343 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001344 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001345 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001346 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001347 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001348 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001349 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001350 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001351 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001352 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001353 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001354 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001355 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001356 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001357 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001358 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001359 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001360 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001361 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001362 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001363 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001364 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001365 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001366 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001367 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001368 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001369 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001370 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001371 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001372 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001373 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001374 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001375 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001376 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001377 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001378 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001379 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001380 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001381 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001382 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001383 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001384 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_rainy_001385 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001386 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001387 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001388 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001389 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001390 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001391 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001392 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001393 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001394 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_rainy_001395 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001396 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001397 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001398 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001399 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001400 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001401 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001402 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_001403 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001404 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001405 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001406 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001407 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001408 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001409 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001410 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_001411 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001412 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001413 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001414 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001415 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001416 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001417 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001418 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001419 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001420 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001421 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001422 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001423 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001424 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001425 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001426 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001427 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001428 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001429 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001430 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001431 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001432 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001433 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001434 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001435 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001436 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001437 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001438 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_001439 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001440 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001441 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001442 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001443 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001444 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001445 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001446 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001447 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001448 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001449 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001450 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001451 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001452 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001453 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001454 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001455 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001456 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001457 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001458 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001459 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001460 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001461 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001462 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001463 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_snowy_001464 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001465 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001466 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001467 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001468 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001469 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_rainy_001470 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001471 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001472 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001473 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001474 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001475 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001476 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001477 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001478 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001479 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001480 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001481 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001482 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001483 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001484 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_night_normal_001485 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001486 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001487 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001488 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001489 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001490 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001491 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001492 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001493 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001494 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001495 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001496 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001497 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001498 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_snowy_001499 | collision_frame | None | accident=1 但 collision_frame=null | B |
| crash_day_normal_001500 | collision_frame | None | accident=1 但 collision_frame=null | B |

## 2. prediction_eligible 规则复核

- prediction_eligible=true：**4796**；false：**175**
- early_motion_peak 标记：**175**（source 分布 {'CARLA': 175}；split 分布 {'train': 175}）
- early 且 prediction_eligible=false：175；false 但非 early：0 条 []
- early 样本 peak_frame_mad<18：175；>=18：0 条 []；无 peak 字段：0（真实样本无 MAD 字段）
- 正样本 true 的碰撞帧分布：{20: 971, None: 486, 7: 1, 13: 1}
- 正样本 true 中碰撞帧在 [18,22] 之外：488 条 ['crash_day_snowy_000005', 'crash_day_snowy_000006', 'crash_day_snowy_000007', 'crash_night_rainy_000010', 'crash_day_rainy_000012', 'crash_day_rainy_000016', 'crash_day_snowy_000017', 'crash_day_snowy_000019', 'crash_day_snowy_000020', 'crash_day_snowy_000021', 'crash_day_snowy_000024', 'crash_day_snowy_000025', 'crash_night_normal_000027', 'crash_day_snowy_000028', 'crash_day_snowy_000029', 'crash_day_snowy_000031', 'crash_night_normal_000032', 'crash_night_snowy_000034', 'crash_night_normal_000035', 'crash_day_snowy_000037', 'crash_day_snowy_000038', 'crash_day_snowy_000039', 'crash_night_normal_000040', 'crash_night_normal_000041', 'crash_day_snowy_000042', 'crash_day_rainy_000045', 'crash_night_snowy_000046', 'crash_day_snowy_000048', 'crash_night_normal_000049', 'crash_night_rainy_000050', 'crash_night_normal_000051', 'crash_night_snowy_000052', 'crash_day_snowy_000053', 'crash_day_snowy_000054', 'crash_day_snowy_000056', 'crash_day_snowy_000057', 'crash_day_snowy_000059', 'crash_day_snowy_000061', 'crash_day_snowy_000063', 'crash_day_snowy_000064', 'crash_day_snowy_000065', 'crash_day_snowy_000068', 'crash_night_normal_000069', 'crash_day_snowy_000071', 'crash_day_snowy_000074', 'crash_day_snowy_000075', 'crash_day_rainy_000077', 'crash_day_snowy_000078', 'crash_day_snowy_000079', 'crash_night_normal_000082', 'crash_day_snowy_000084', 'crash_night_snowy_000086', 'crash_day_snowy_000087', 'crash_day_snowy_000088', 'crash_day_snowy_000089', 'crash_day_snowy_000090', 'crash_night_normal_000091', 'crash_night_normal_000092', 'crash_day_snowy_000093', 'crash_day_snowy_000094', 'crash_night_normal_000095', 'crash_day_rainy_000102', 'crash_day_snowy_000103', 'crash_night_normal_000104', 'crash_day_snowy_000105', 'crash_day_snowy_000106', 'crash_day_snowy_000111', 'crash_day_snowy_000112', 'crash_day_snowy_000113', 'crash_day_snowy_000114', 'crash_day_rainy_000115', 'crash_day_snowy_000116', 'crash_day_snowy_000119', 'crash_day_rainy_000121', 'crash_day_rainy_000122', 'crash_day_snowy_000124', 'crash_day_rainy_000125', 'crash_night_normal_000126', 'crash_day_rainy_000127', 'crash_night_normal_000128', 'crash_day_snowy_000131', 'crash_day_snowy_000132', 'crash_day_snowy_000133', 'crash_day_rainy_000134', 'crash_day_snowy_000135', 'crash_day_snowy_000136', 'crash_night_rainy_000139', 'crash_day_snowy_000140', 'crash_day_snowy_000143', 'crash_night_normal_000145', 'crash_day_snowy_000147', 'crash_day_rainy_000148', 'crash_day_snowy_000155', 'crash_day_rainy_000169', 'crash_day_rainy_000180', 'crash_day_rainy_000188', 'crash_day_rainy_000201', 'crash_night_normal_000204', 'crash_day_rainy_000207', 'crash_night_normal_000208', 'crash_night_normal_000210', 'crash_night_rainy_000212', 'crash_night_normal_000216', 'crash_day_snowy_000219', 'crash_day_snowy_000220', 'crash_night_snowy_000221', 'crash_day_snowy_000222', 'crash_day_snowy_000223', 'crash_day_snowy_000225', 'crash_day_snowy_000226', 'crash_day_snowy_000228', 'crash_night_normal_000229', 'crash_day_snowy_000230', 'crash_night_normal_000231', 'crash_day_rainy_000232', 'crash_day_snowy_000233', 'crash_day_snowy_000236', 'crash_night_normal_000238', 'crash_day_snowy_000239', 'crash_day_snowy_000247', 'crash_day_snowy_000255', 'crash_day_snowy_000256', 'crash_night_normal_000289', 'crash_day_rainy_000290', 'crash_day_snowy_000291', 'crash_day_snowy_000293', 'crash_day_snowy_000294', 'crash_day_snowy_000295', 'crash_night_normal_000297', 'crash_day_snowy_000298', 'crash_day_snowy_000299', 'crash_day_rainy_000302', 'crash_day_snowy_000303', 'crash_day_rainy_000304', 'crash_day_snowy_000307', 'crash_day_snowy_000310', 'crash_day_snowy_000313', 'crash_night_normal_000314', 'crash_night_normal_000318', 'crash_day_snowy_000320', 'crash_night_normal_000321', 'crash_night_normal_000329', 'crash_day_rainy_000343', 'crash_night_normal_000348', 'crash_day_rainy_000351', 'crash_day_rainy_000356', 'crash_night_rainy_000357', 'crash_night_normal_000359', 'crash_day_rainy_000364', 'crash_day_rainy_000365', 'crash_night_normal_000369', 'crash_night_normal_000371', 'crash_day_rainy_000372', 'crash_day_rainy_000374', 'crash_night_normal_000378', 'crash_day_snowy_000379', 'crash_day_snowy_000381', 'crash_night_normal_000382', 'crash_night_normal_000383', 'crash_night_normal_000384', 'crash_night_normal_000385', 'crash_day_snowy_000386', 'crash_day_snowy_000387', 'crash_night_snowy_000388', 'crash_night_normal_000389', 'crash_day_rainy_000391', 'crash_night_normal_000392', 'crash_day_rainy_000393', 'crash_day_snowy_000394', 'crash_night_snowy_000395', 'crash_day_rainy_000396', 'crash_night_normal_000397', 'crash_day_snowy_000398', 'crash_day_snowy_000399', 'crash_day_snowy_000400', 'crash_night_snowy_000401', 'crash_day_snowy_000402', 'crash_day_snowy_000403', 'crash_day_rainy_000405', 'crash_day_snowy_000407', 'crash_day_snowy_000408', 'crash_day_snowy_000410', 'crash_night_normal_000411', 'crash_day_rainy_000415', 'crash_day_snowy_000420', 'crash_day_rainy_000424', 'crash_day_rainy_000438', 'crash_night_rainy_000447', 'crash_day_snowy_000450', 'crash_night_normal_000455', 'crash_day_snowy_000456', 'crash_day_rainy_000468', 'crash_day_snowy_000470', 'crash_day_snowy_000472', 'crash_day_snowy_000473', 'crash_day_rainy_000477', 'crash_night_rainy_000492', 'crash_day_snowy_000493', 'crash_day_snowy_000494', 'crash_day_snowy_000496', 'crash_day_snowy_000499', 'crash_day_snowy_000500', 'crash_night_normal_000502', 'crash_night_normal_000503', 'crash_night_rainy_000504', 'crash_night_normal_000505', 'crash_night_normal_000506', 'crash_night_normal_000507', 'crash_night_snowy_000508', 'crash_night_snowy_000509', 'crash_night_normal_000510', 'crash_night_normal_000511', 'crash_night_snowy_000512', 'crash_night_normal_000513', 'crash_night_normal_000514', 'crash_day_rainy_000515', 'crash_day_snowy_000518', 'crash_day_snowy_000520', 'crash_day_snowy_000521', 'crash_day_rainy_000522', 'crash_night_snowy_000526', 'crash_day_rainy_000529', 'crash_night_snowy_000531', 'crash_night_normal_000532', 'crash_night_normal_000533', 'crash_night_normal_000534', 'crash_night_normal_000535', 'crash_night_rainy_000536', 'crash_night_rainy_000537', 'crash_day_rainy_000546', 'crash_day_snowy_000547', 'crash_day_snowy_000549', 'crash_day_snowy_000550', 'crash_day_snowy_000551', 'crash_night_normal_000552', 'crash_night_rainy_000553', 'crash_day_rainy_000557', 'crash_day_rainy_000560', 'crash_night_normal_000563', 'crash_day_rainy_000583', 'crash_night_normal_000592', 'crash_night_normal_000593', 'crash_night_normal_000594', 'crash_night_normal_000596', 'crash_night_normal_000610', 'crash_day_rainy_000611', 'crash_day_snowy_000616', 'crash_day_snowy_000617', 'crash_night_snowy_000619', 'crash_night_normal_000624', 'crash_night_normal_000625', 'crash_night_normal_000626', 'crash_night_normal_000627', 'crash_night_normal_000637', 'crash_night_normal_000638', 'crash_day_snowy_000643', 'crash_day_snowy_000644', 'crash_day_snowy_000645', 'crash_day_snowy_000646', 'crash_day_snowy_000647', 'crash_night_normal_000648', 'crash_night_snowy_000649', 'crash_night_snowy_000650', 'crash_night_normal_000651', 'crash_night_normal_000652', 'crash_night_snowy_000653', 'crash_night_normal_000662', 'crash_day_snowy_000672', 'crash_night_rainy_000674', 'crash_day_snowy_000675', 'crash_day_snowy_000691', 'crash_night_rainy_000696', 'crash_night_rainy_000701', 'crash_night_normal_000704', 'crash_day_snowy_000715', 'crash_day_snowy_000718', 'crash_night_normal_000719', 'crash_night_normal_000721', 'crash_day_snowy_000724', 'crash_day_rainy_000730', 'crash_night_normal_000731', 'crash_day_rainy_000735', 'crash_night_rainy_000739', 'crash_day_rainy_000740', 'crash_night_normal_000745', 'crash_day_rainy_000746', 'crash_night_normal_000747', 'crash_day_rainy_000778', 'crash_night_normal_000782', 'crash_day_rainy_000784', 'crash_day_rainy_000789', 'crash_day_rainy_000808', 'crash_day_rainy_000822', 'crash_day_rainy_000827', 'crash_day_rainy_000828', 'crash_day_rainy_000859', 'crash_night_normal_000861', 'crash_night_normal_000866', 'crash_day_rainy_000867', 'crash_day_rainy_000870', 'crash_night_normal_000875', 'crash_day_rainy_000879', 'crash_night_normal_000880', 'crash_day_rainy_000886', 'crash_day_rainy_000897', 'crash_night_normal_000918', 'crash_night_normal_000930', 'crash_night_snowy_000931', 'crash_night_normal_000935', 'crash_day_rainy_000940', 'crash_day_rainy_000945', 'crash_day_rainy_000947', 'crash_day_rainy_000956', 'crash_day_rainy_000971', 'crash_day_rainy_000983', 'crash_night_normal_000989', 'crash_night_normal_000990', 'crash_day_rainy_000991', 'crash_day_snowy_000999', 'crash_night_normal_001001', 'crash_day_rainy_001005', 'crash_day_snowy_001010', 'crash_night_snowy_001014', 'crash_night_normal_001018', 'crash_day_rainy_001022', 'crash_day_rainy_001024', 'crash_night_normal_001026', 'crash_night_snowy_001028', 'crash_day_snowy_001030', 'crash_day_snowy_001038', 'crash_night_normal_001039', 'crash_day_snowy_001040', 'crash_day_snowy_001043', 'crash_day_snowy_001048', 'crash_night_normal_001052', 'crash_night_normal_001053', 'crash_day_snowy_001057', 'crash_day_snowy_001060', 'crash_day_rainy_001064', 'crash_night_normal_001068', 'crash_day_snowy_001069', 'crash_day_snowy_001078', 'crash_day_snowy_001088', 'crash_day_snowy_001089', 'crash_day_rainy_001090', 'crash_day_rainy_001091', 'crash_night_normal_001095', 'crash_day_rainy_001096', 'crash_day_rainy_001097', 'crash_night_rainy_001100', 'crash_night_normal_001101', 'crash_day_rainy_001104', 'crash_day_snowy_001105', 'crash_night_snowy_001110', 'crash_day_snowy_001111', 'crash_night_normal_001112', 'crash_night_snowy_001113', 'crash_day_snowy_001115', 'crash_day_rainy_001121', 'crash_day_snowy_001122', 'crash_day_snowy_001123', 'crash_day_snowy_001125', 'crash_day_snowy_001126', 'crash_day_snowy_001127', 'crash_day_snowy_001128', 'crash_night_snowy_001130', 'crash_night_normal_001132', 'crash_day_snowy_001133', 'crash_night_normal_001134', 'crash_night_snowy_001137', 'crash_night_normal_001138', 'crash_day_snowy_001140', 'crash_day_snowy_001144', 'crash_night_normal_001149', 'crash_day_snowy_001150', 'crash_day_snowy_001151', 'crash_night_normal_001152', 'crash_night_normal_001154', 'crash_night_normal_001155', 'crash_day_snowy_001156', 'crash_night_normal_001159', 'crash_day_snowy_001161', 'crash_day_snowy_001163', 'crash_night_normal_001165', 'crash_night_snowy_001167', 'crash_day_snowy_001170', 'crash_day_snowy_001174', 'crash_day_snowy_001175', 'crash_night_snowy_001176', 'crash_day_snowy_001177', 'crash_day_snowy_001178', 'crash_day_snowy_001179', 'crash_day_snowy_001180', 'crash_night_normal_001182', 'crash_day_snowy_001193', 'crash_day_snowy_001194', 'crash_night_normal_001195', 'crash_day_snowy_001196', 'crash_day_rainy_001201', 'crash_day_rainy_001207', 'crash_day_rainy_001209', 'crash_night_normal_001210', 'crash_night_normal_001211', 'crash_day_rainy_001218', 'crash_night_normal_001224', 'crash_day_rainy_001226', 'crash_day_rainy_001230', 'crash_night_normal_001235', 'crash_day_rainy_001242', 'crash_day_rainy_001249', 'crash_night_normal_001258', 'crash_day_rainy_001260', 'crash_day_rainy_001266', 'crash_day_rainy_001278', 'crash_night_normal_001288', 'crash_night_normal_001292', 'crash_day_rainy_001310', 'crash_night_normal_001311', 'crash_night_normal_001312', 'crash_day_rainy_001323', 'crash_day_rainy_001327', 'crash_day_rainy_001337', 'crash_night_normal_001338', 'crash_day_rainy_001342', 'crash_day_rainy_001348', 'crash_night_normal_001352', 'crash_day_snowy_001353', 'crash_day_rainy_001356', 'crash_night_normal_001364', 'crash_day_snowy_001367', 'crash_night_normal_001371', 'crash_day_rainy_001376', 'crash_night_rainy_001385', 'crash_day_rainy_001386', 'crash_day_rainy_001390', 'crash_day_snowy_001392', 'crash_day_snowy_001394', 'crash_night_rainy_001395', 'crash_night_normal_001400', 'crash_night_snowy_001403', 'crash_night_snowy_001411', 'crash_day_snowy_001415', 'crash_day_snowy_001417', 'crash_day_snowy_001418', 'crash_day_rainy_001420', 'crash_day_snowy_001422', 'crash_day_rainy_001427', 'crash_day_snowy_001429', 'crash_day_rainy_001430', 'crash_day_snowy_001431', 'crash_day_rainy_001432', 'crash_night_normal_001434', 'crash_day_snowy_001436', 'crash_night_normal_001437', 'crash_night_snowy_001439', 'crash_day_snowy_001446', 'crash_day_snowy_001447', 'crash_day_snowy_001448', 'crash_day_snowy_001451', 'crash_day_rainy_001453', 'crash_day_snowy_001455', 'crash_day_snowy_001462', 'crash_night_snowy_001464', 'crash_day_snowy_001467', 'crash_day_snowy_001469', 'crash_day_rainy_001470', 'crash_day_snowy_001472', 'crash_day_snowy_001473', 'crash_day_snowy_001474', 'crash_day_snowy_001475', 'crash_day_snowy_001477', 'crash_day_snowy_001478', 'crash_day_snowy_001479', 'crash_day_snowy_001480', 'crash_day_snowy_001481', 'crash_night_normal_001485', 'crash_day_snowy_001486', 'crash_day_snowy_001487', 'crash_day_snowy_001488', 'crash_day_snowy_001491', 'crash_day_snowy_001492', 'crash_day_snowy_001493', 'crash_day_snowy_001494', 'crash_day_snowy_001496', 'crash_day_snowy_001498', 'crash_day_snowy_001499', 'dada_39_013', 'dada_11_082']
- 真实正样本碰撞帧分布：{None: 486, 20: 23, 7: 1, 13: 1}
- 负样本 true：3337（语义说明见 json）

## 3. 划分互斥

| 集合对 | ID 重叠 | group 重叠 | 视频重叠 |
|---|---|---|---|
| reserve/test_real | 0 | 0 | 0 |
| reserve/train | 0 | 0 | 0 |
| reserve/val_real | 0 | 0 | 0 |
| test_real/train | 0 | 0 | 0 |
| test_real/val_real | 0 | 0 | 0 |
| train/val_real | 0 | 0 | 0 |

## 4. 类别分布（全库）

| 维度 | 分布 |
|---|---|
| total | 4971 |
| split | {"train": 2700, "reserve": 1731, "val_real": 200, "test_real": 340} |
| target | {"pos": 1591, "neg": 3380} |
| domain | {"synthetic": 2700, "real": 2271} |
| weather | {"rainy": 885, "snowy": 987, "night": 1545, "clear": 1554} |
| source | {"CARLA": 2700, "CCD": 1500, "DADA": 25, "BDD100K": 746} |
| accident | {"1": 3145, "0": 1826} |
| negative_type | {"None": 1591, "adverse_no_accident": 1826, "clear_accident": 1554} |
| prediction_eligible | {"false": 175, "true": 4796} |
| scenario | {"rear_end": 900, "side_impact": 900, "pedestrian": 900, "unknown": 2271} |

### 关键组合

| 组合 | 数量 |
|---|---|
| real_accident | 1525 |
| real_nonaccident | 746 |
| syn_accident | 1620 |
| syn_nonaccident | 1080 |
| rainy_accident | 476 |
| snowy_accident | 565 |
| night_accident | 550 |
| rainy_night_accident | 476 |
| adverse_accident | 1591 |
| adverse_nonaccident | 1826 |
| pe_true_real_accident | 1525 |
| pe_true_adverse_accident | 1459 |
| clear_accident_total | 1554 |

## 5. 每 split 统计

### train

```
{
  "total": 2700,
  "pos": 1350,
  "neg": 1350,
  "accident_rate": 0.75,
  "day_night": {
    "night": 768,
    "day": 1932
  },
  "weather": {
    "rainy": 583,
    "snowy": 674,
    "night": 768,
    "clear": 675
  },
  "domain": {
    "synthetic": 2160,
    "real": 540
  },
  "prediction_eligible": {
    "false": 175,
    "true": 2525
  },
  "negative_type": {
    "None": 1350,
    "adverse_no_accident": 675,
    "clear_accident": 675
  }
}
```

### val_real

```
{
  "total": 200,
  "pos": 100,
  "neg": 100,
  "accident_rate": 0.75,
  "day_night": {
    "night": 87,
    "day": 113
  },
  "weather": {
    "clear": 50,
    "snowy": 26,
    "night": 87,
    "rainy": 37
  },
  "domain": {
    "real": 200
  },
  "prediction_eligible": {
    "true": 200
  },
  "negative_type": {
    "clear_accident": 50,
    "None": 100,
    "adverse_no_accident": 50
  }
}
```

### test_real

```
{
  "total": 340,
  "pos": 140,
  "neg": 200,
  "accident_rate": 0.5882,
  "day_night": {
    "night": 110,
    "day": 230
  },
  "weather": {
    "snowy": 90,
    "clear": 60,
    "rainy": 80,
    "night": 110
  },
  "domain": {
    "real": 340
  },
  "prediction_eligible": {
    "true": 340
  },
  "negative_type": {
    "None": 140,
    "clear_accident": 60,
    "adverse_no_accident": 140
  }
}
```

### reserve

```
{
  "total": 1731,
  "pos": 1,
  "neg": 1730,
  "accident_rate": 0.4448,
  "day_night": {
    "night": 580,
    "day": 1151
  },
  "weather": {
    "rainy": 185,
    "snowy": 197,
    "night": 580,
    "clear": 769
  },
  "domain": {
    "synthetic": 540,
    "real": 1191
  },
  "prediction_eligible": {
    "true": 1731
  },
  "negative_type": {
    "adverse_no_accident": 961,
    "clear_accident": 769,
    "None": 1
  }
}
```

## 6. 元数据缺口

- **camera_type**：manifest 无 camera 字段（实际来源均为前视行车记录仪视角）→ C 级元数据缺口
- **day_night**：manifest 无 day/night 字段；本审计按 weather=night→night、其余→day 映射统计
- **source_url**：manifest 无 source URL 字段 → 无法直接验证链接，靠 original_video_id/本地源文件追溯
- **fog**：weather 无 fog 类（源数据不含雾天）

## 7. 结论

**ISSUES_FOUND**
