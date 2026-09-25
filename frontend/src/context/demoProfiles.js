// Official Demo Administrative Officer Profiles & V.3 Demo Account

export const V3_DEMO_EMAIL = 'v.3@gmail.com';

export const V3_DEMO_PROFILE = {
  id: 'off-v3',
  name: 'V.3 Analytical Evaluator',
  email: V3_DEMO_EMAIL,
  designation: 'Demonstration & Simulation Sandbox',
  ministry: 'MoSPI / IPMD Analytical Sandbox',
  role: 'Demo Mode Evaluator',
  departmentCode: 'V3-SANDBOX-LAB',
  clearanceLevel: 'Level-Special (Simulation)',
  avatar: 'V3',
  isDemoAccount: true,
};

export const OFFICIAL_PROFILES = [
  {
    id: 'off-001',
    name: 'Dr. Rajesh Sharma, IAS',
    email: 'rajesh.sharma@mospi.gov.in',
    designation: 'Joint Secretary (IPMD)',
    ministry: 'Ministry of Statistics and Programme Implementation',
    role: 'Cabinet Review Authority',
    departmentCode: 'MoSPI-IPMD-01',
    clearanceLevel: 'Level-5 (Cabinet Secretariat)',
    avatar: 'RS',
  },
  {
    id: 'off-002',
    name: 'Pooja Verma, IDAS',
    email: 'p.verma@nhai.gov.in',
    designation: 'Chief General Manager (Coordination)',
    ministry: 'Ministry of Road Transport and Highways',
    role: 'Implementing Authority',
    departmentCode: 'MoRTH-NHAI-HQ',
    clearanceLevel: 'Level-3 (Nodal Project Oversight)',
    avatar: 'PV',
  },
  {
    id: 'off-003',
    name: 'Vikramaditya Sengupta',
    email: 'v.sengupta@railnet.gov.in',
    designation: 'Executive Director (Works)',
    ministry: 'Ministry of Railways',
    role: 'Implementing Authority',
    departmentCode: 'MoR-RB-WORKS',
    clearanceLevel: 'Level-4 (Zonal Infrastructure)',
    avatar: 'VS',
  },
  {
    id: 'off-004',
    name: 'Dr. Ananya Iyer',
    email: 'ananya.iyer@niti.gov.in',
    designation: 'Senior Infrastructure Policy Specialist',
    ministry: 'NITI Aayog / Cabinet Secretariat',
    role: 'Policy & Analytics Specialist',
    departmentCode: 'NITI-INFRA-DMEO',
    clearanceLevel: 'Level-4 (Public Policy Evaluation)',
    avatar: 'AI',
  }
];

export const MOSPI_ADMIN_PROFILE = {
  id: 'usr-admin-01',
  name: 'MoSPI Registry Official',
  email: 'admin@mospi.gov.in',
  designation: 'MoSPI Registry Official',
  ministry: 'MoSPI Infrastructure Monitoring Division',
  role: 'admin',
  departmentCode: 'MoSPI-IPMD-HQ',
  clearanceLevel: 'Level-5 (Cabinet Secretariat)',
  avatar: 'RO',
};

export const DEMO_PROFILES = [MOSPI_ADMIN_PROFILE, V3_DEMO_PROFILE, ...OFFICIAL_PROFILES];

export const CANONICAL_MINISTRIES = [
  'Ministry of Road Transport and Highways',
  'Ministry of Railways',
  'Ministry of Power',
  'Ministry of Petroleum and Natural Gas',
  'Ministry of Coal',
  'Ministry of Housing and Urban Affairs',
  'Ministry of Civil Aviation',
  'Ministry of Steel',
  'Ministry of Health and Family Welfare',
  'Department of Higher Education',
  'Department of Telecommunications',
  'Department of Water Resources, River Development and GR',
  'Department for Promotion of Industry and Internal Trade',
  'Ministry of Mines',
  'Ministry of Ports, Shipping and Waterways',
  'Ministry of Labour and Employment',
  'Ministry of Statistics and Programme Implementation (MoSPI)'
];

export default DEMO_PROFILES;
