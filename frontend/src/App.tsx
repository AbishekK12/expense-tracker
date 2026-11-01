import { useEffect, useMemo, useState } from 'react'
import type { ReactNode, FormEvent } from 'react'
import { LayoutDashboard, ArrowLeftRight, Wallet, Tags, Target, ChartNoAxesCombined, FileText, Plus, Search, Trash2, Pencil, X, Menu, RefreshCw, IndianRupee, TrendingUp, TrendingDown, CircleDollarSign } from 'lucide-react'
import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis, PieChart, Pie, Cell } from 'recharts'
import { api } from './api'

type Expense = { id:string; description:string; amount:number; category:string; expense_date:string }
type Income = { id:string; description:string; amount:number; source:string; income_date:string }
type Category = { id:string; name:string; kind:'expense'|'income'|'both'; color:string }
type Budget = { id:string; category:string; month:string; amount:number; spent:number; remaining:number; over_budget:boolean }
type Summary = { month:string; income:number; expenses:number; balance:number; all_time_income:number; all_time_expenses:number; all_time_balance:number; transaction_count:number; recent_transactions:{id:string;type:string;description:string;category:string;amount:number;date:string}[] }
type Tab = 'Overview'|'Transactions'|'Income'|'Categories'|'Budgets'|'Analytics'|'Reports'

const money = (v:number) => new Intl.NumberFormat('en-IN',{style:'currency',currency:'INR',maximumFractionDigits:2}).format(v || 0)
const today = () => new Date().toISOString().slice(0,10)
const monthNow = () => today().slice(0,7)
const nav = [
  {name:'Overview' as Tab, icon:LayoutDashboard},
  {name:'Transactions' as Tab, icon:ArrowLeftRight},
  {name:'Income' as Tab, icon:Wallet},
  {name:'Categories' as Tab, icon:Tags},
  {name:'Budgets' as Tab, icon:Target},
  {name:'Analytics' as Tab, icon:ChartNoAxesCombined},
  {name:'Reports' as Tab, icon:FileText},
]
const palette = ['#6c63ff','#19b88a','#f5a524','#ef6b73','#3ba5d9','#9b7bea']

export default function App() {
  const [tab,setTab] = useState<Tab>('Overview')
  const [mobile,setMobile] = useState(false)
  const [month,setMonth] = useState(monthNow())
  const [expenses,setExpenses] = useState<Expense[]>([])
  const [income,setIncome] = useState<Income[]>([])
  const [categories,setCategories] = useState<Category[]>([])
  const [budgets,setBudgets] = useState<Budget[]>([])
  const [summary,setSummary] = useState<Summary | null>(null)
  const [monthly,setMonthly] = useState<any[]>([])
  const [categoryStats,setCategoryStats] = useState<any[]>([])
  const [report,setReport] = useState<any>(null)
  const [loading,setLoading] = useState(false)
  const [error,setError] = useState('')
  const [notice,setNotice] = useState('')
  const [search,setSearch] = useState('')
  const [modal,setModal] = useState<'expense'|'income'|'category'|'budget'|null>(null)
  const [editing,setEditing] = useState<any>(null)

  async function loadAll() {
    setLoading(true); setError('')
    try {
      const [e,i,c,b,s,m,cs,r] = await Promise.all([
        api.get<{items:Expense[]}>('/api/expenses?limit=200'),
        api.get<{items:Income[]}>('/api/income?limit=200'),
        api.get<{items:Category[]}>('/api/categories'),
        api.get<{items:Budget[]}>(`/api/budgets?month=${month}`),
        api.get<Summary>(`/api/dashboard/summary?month=${month}`),
        api.get<any>(`/api/analytics/monthly?year=${month.slice(0,4)}`),
        api.get<any>(`/api/analytics/categories?month=${month}`),
        api.get<any>('/api/reports'),
      ])
      setExpenses(e.items); setIncome(i.items); setCategories(c.items); setBudgets(b.items)
      setSummary(s); setMonthly(m.items); setCategoryStats(cs.items); setReport(r)
    } catch (err) { setError(err instanceof Error ? err.message : 'Unable to load application data.') }
    finally { setLoading(false) }
  }
  useEffect(()=>{ loadAll() },[month])
  useEffect(()=>{ if(notice){const t=setTimeout(()=>setNotice(''),3000);return ()=>clearTimeout(t)} },[notice])

  async function saveRecord(kind:'expense'|'income'|'category'|'budget', payload:any) {
    try {
      const base = kind==='expense'?'/api/expenses':kind==='income'?'/api/income':kind==='category'?'/api/categories':'/api/budgets'
      if(editing?.id) await api.put(`${base}/${editing.id}`,payload)
      else await api.post(base,payload)
      setModal(null);setEditing(null);setNotice(`${kind[0].toUpperCase()+kind.slice(1)} saved successfully.`);await loadAll()
    } catch(err){setError(err instanceof Error?err.message:'Unable to save record.')}
  }
  async function remove(kind:'expense'|'income'|'category'|'budget', id:string) {
    if(!window.confirm('Delete this record? This action cannot be undone.')) return
    const base = kind==='expense'?'/api/expenses':kind==='income'?'/api/income':kind==='category'?'/api/categories':'/api/budgets'
    try { await api.delete(`${base}/${id}`);setNotice('Record deleted.');await loadAll() } catch(err){setError(err instanceof Error?err.message:'Unable to delete record.')}
  }
  const filteredExpenses = useMemo(()=>expenses.filter(x=>[x.description,x.category].join(' ').toLowerCase().includes(search.toLowerCase())),[expenses,search])
  const filteredIncome = useMemo(()=>income.filter(x=>[x.description,x.source].join(' ').toLowerCase().includes(search.toLowerCase())),[income,search])
  const openModal=(kind:'expense'|'income'|'category'|'budget',record:any=null)=>{setEditing(record);setModal(kind)}

  return <div className="app-shell">
    <aside className={`sidebar ${mobile?'open':''}`}>
      <div className="brand"><div className="brand-mark"><IndianRupee size={21}/></div><div><b>PaisaFlow</b><small>PERSONAL FINANCE</small></div><button className="mobile-close" onClick={()=>setMobile(false)}><X/></button></div>
      <div className="nav-label">WORKSPACE</div>
      <nav>{nav.map(item=><button key={item.name} className={`nav-item ${tab===item.name?'active':''}`} onClick={()=>{setTab(item.name);setMobile(false)}}><item.icon size={18}/><span>{item.name}</span>{item.name==='Transactions'&&<small>{expenses.length}</small>}</button>)}</nav>
      <div className="sidebar-bottom"><div className="currency-chip"><span className="dot"/> INR · Indian Rupee</div><small>Local data storage · v1.0</small></div>
    </aside>
    {mobile&&<div className="scrim" onClick={()=>setMobile(false)}/>}
    <main className="main">
      <header className="topbar"><button className="menu-button" onClick={()=>setMobile(true)}><Menu/></button><div><span className="eyebrow">PERSONAL FINANCE</span><h1>{tab}</h1></div><div className="top-actions"><label className="month-picker"> <span>Period</span><input type="month" value={month} onChange={e=>setMonth(e.target.value)}/></label><button className="icon-button" title="Refresh data" onClick={loadAll}><RefreshCw size={17}/></button><button className="primary-button" onClick={()=>openModal('expense')}><Plus size={17}/> Add expense</button></div></header>
      {error&&<div className="alert error">{error}<button onClick={()=>setError('')}><X size={16}/></button></div>}
      {notice&&<div className="alert success">{notice}</div>}
      {loading&&<div className="loading-line"/>}
      {tab==='Overview'&&<Overview summary={summary} budgets={budgets} monthly={monthly} onAdd={()=>openModal('expense')} onTab={setTab}/>}
      {tab==='Transactions'&&<section className="panel"><PanelHead title="Expense transactions" subtitle="Review, search, edit and remove your expenses" action={<button className="primary-button" onClick={()=>openModal('expense')}><Plus size={16}/> Add expense</button>}/><SearchBox value={search} onChange={setSearch}/><ExpenseTable rows={filteredExpenses} onEdit={r=>openModal('expense',r)} onDelete={id=>remove('expense',id)}/></section>}
      {tab==='Income'&&<section className="panel"><PanelHead title="Income sources" subtitle="Track salary, freelance work and other income" action={<button className="primary-button" onClick={()=>openModal('income')}><Plus size={16}/> Add income</button>}/><SearchBox value={search} onChange={setSearch}/><IncomeTable rows={filteredIncome} onEdit={r=>openModal('income',r)} onDelete={id=>remove('income',id)}/></section>}
      {tab==='Categories'&&<section className="panel"><PanelHead title="Categories" subtitle="Organize spending and income sources" action={<button className="primary-button" onClick={()=>openModal('category')}><Plus size={16}/> Add category</button>}/><div className="category-grid">{categories.map(c=><div className="category-card" key={c.id}><span className="category-swatch" style={{background:c.color}}/><div><b>{c.name}</b><small>{c.kind}</small></div><div className="row-actions"><button onClick={()=>openModal('category',c)}><Pencil size={15}/></button><button onClick={()=>remove('category',c.id)}><Trash2 size={15}/></button></div></div>)}{!categories.length&&<Empty text="No categories yet. Add one to organize your records."/>}</div></section>}
      {tab==='Budgets'&&<section className="panel"><PanelHead title="Monthly budgets" subtitle="Set spending limits and monitor category usage" action={<button className="primary-button" onClick={()=>openModal('budget')}><Plus size={16}/> Create budget</button>}/><div className="budget-list">{budgets.map(b=><div className="budget-row" key={b.id}><div className="budget-head"><div><b>{b.category}</b><small>{b.month}</small></div><div className="budget-numbers"><b>{money(b.spent)} <span>/ {money(b.amount)}</span></b><small>{b.over_budget?'Over budget':money(b.remaining)+' remaining'}</small></div></div><div className="progress"><i className={b.over_budget?'over':''} style={{width:`${Math.min(100,b.spent/b.amount*100)}%`}}/></div><div className="budget-foot"><small>{Math.round(b.spent/b.amount*100)}% used</small><div className="row-actions"><button onClick={()=>openModal('budget',b)}><Pencil size={15}/></button><button onClick={()=>remove('budget',b.id)}><Trash2 size={15}/></button></div></div></div>)}{!budgets.length&&<Empty text="No budgets for this month. Create your first budget."/>}</div></section>}
      {tab==='Analytics'&&<Analytics monthly={monthly} categories={categoryStats} month={month}/>}
      {tab==='Reports'&&<section className="panel"><PanelHead title="Financial report" subtitle="All-time summary based on your saved records"/><div className="report-summary"><ReportMetric label="Total income" value={money(report?.total_income||0)}/><ReportMetric label="Total expenses" value={money(report?.total_expenses||0)}/><ReportMetric label="Net balance" value={money(report?.net_balance||0)}/></div><div className="report-actions"><button className="secondary-button" onClick={()=>downloadReport(report)}>Export report as CSV</button></div><h3 className="subheading">Included records</h3><p className="muted">{report?.income_count||0} income records · {report?.expense_count||0} expense records</p></section>}
    </main>
    {modal&&<RecordModal kind={modal} initial={editing} categories={categories} month={month} onClose={()=>{setModal(null);setEditing(null)}} onSave={payload=>saveRecord(modal,payload)}/>}
  </div>
}

function PanelHead({title,subtitle,action}:{title:string;subtitle:string;action?:ReactNode}){return <div className="panel-head"><div><h2>{title}</h2><p>{subtitle}</p></div>{action}</div>}
function SearchBox({value,onChange}:{value:string;onChange:(s:string)=>void}){return <div className="search-box"><Search size={17}/><input placeholder="Search description or category..." value={value} onChange={e=>onChange(e.target.value)}/></div>}
function Empty({text}:{text:string}){return <div className="empty"><div className="empty-icon"><CircleDollarSign/></div><b>Nothing here yet</b><span>{text}</span></div>}
function Metric({label,value,detail,icon:Icon,tone}:{label:string;value:number;detail:string;icon:any;tone:string}){return <div className="metric-card"><div className={`metric-icon ${tone}`}><Icon size={19}/></div><span>{label}</span><strong>{money(value)}</strong><small>{detail}</small></div>}
function Overview({summary,budgets,monthly,onAdd,onTab}:{summary:Summary|null;budgets:Budget[];monthly:any[];onAdd:()=>void;onTab:(t:Tab)=>void}){return <div className="content-stack"><div className="welcome-row"><div><h2>Your money, in focus.</h2><p>A clear view of your monthly financial health.</p></div><button className="secondary-button" onClick={()=>onTab('Reports')}>View reports <span>→</span></button></div><div className="metrics"><Metric label="Monthly income" value={summary?.income||0} detail="Money received this month" icon={TrendingUp} tone="green"/><Metric label="Monthly expenses" value={summary?.expenses||0} detail="Money spent this month" icon={TrendingDown} tone="red"/><Metric label="Monthly balance" value={summary?.balance||0} detail="Income minus expenses" icon={Wallet} tone="purple"/><Metric label="Transactions" value={summary?.transaction_count||0} detail="Records this month" icon={ArrowLeftRight} tone="amber"/></div><div className="dashboard-grid"><div className="panel chart-panel"><PanelHead title="Cash flow" subtitle="Income vs expenses across the selected year"/><div className="chart"><ResponsiveContainer width="100%" height="100%"><BarChart data={monthly}><CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#edf0f5"/><XAxis dataKey="month" tickFormatter={(v)=>v.slice(5)} axisLine={false} tickLine={false}/><YAxis axisLine={false} tickLine={false} tickFormatter={v=>`₹${v/1000}k`}/><Tooltip formatter={(v:any)=>money(Number(v))}/><Legend/><Bar dataKey="income" name="Income" fill="#18b889" radius={[5,5,0,0]}/><Bar dataKey="expenses" name="Expenses" fill="#f17c83" radius={[5,5,0,0]}/></BarChart></ResponsiveContainer></div></div><div className="panel"><PanelHead title="Budget watch" subtitle="Your monthly spending limits"/>{budgets.length?budgets.slice(0,4).map(b=><div className="mini-budget" key={b.id}><div><b>{b.category}</b><small>{money(b.spent)} of {money(b.amount)}</small></div><div className="progress"><i className={b.over_budget?'over':''} style={{width:`${Math.min(100,b.spent/b.amount*100)}%`}}/></div></div>):<Empty text="Create a budget to keep spending on track."/>}<button className="text-button" onClick={()=>onTab('Budgets')}>Manage budgets →</button></div></div><div className="panel"><PanelHead title="Recent activity" subtitle="Your latest income and expense records"/><div className="activity-list">{summary?.recent_transactions?.length?summary.recent_transactions.map((t,i)=><div className="activity-row" key={t.id||i}><div className={`activity-icon ${t.type}`}>{t.type==='income'?<TrendingUp size={17}/>:<TrendingDown size={17}/>}</div><div className="activity-desc"><b>{t.description}</b><small>{t.category} · {t.date}</small></div><strong className={t.type==='income'?'positive':'negative'}>{t.type==='income'?'+':'−'}{money(t.amount)}</strong></div>):<Empty text="Add your first transaction to see activity."/>}</div></div><button className="primary-button" onClick={onAdd}><Plus size={16}/> Add an expense</button></div>}
function ExpenseTable({rows,onEdit,onDelete}:{rows:Expense[];onEdit:(r:Expense)=>void;onDelete:(id:string)=>void}){return <div className="table-wrap"><table><thead><tr><th>Description</th><th>Category</th><th>Date</th><th>Amount</th><th/></tr></thead><tbody>{rows.map(r=><tr key={r.id}><td><b>{r.description}</b></td><td><span className="tag">{r.category}</span></td><td>{r.expense_date}</td><td className="amount">{money(r.amount)}</td><td><div className="row-actions"><button onClick={()=>onEdit(r)}><Pencil size={15}/></button><button onClick={()=>onDelete(r.id)}><Trash2 size={15}/></button></div></td></tr>)}</tbody></table>{!rows.length&&<Empty text="No matching expenses found."/>}</div>}
function IncomeTable({rows,onEdit,onDelete}:{rows:Income[];onEdit:(r:Income)=>void;onDelete:(id:string)=>void}){return <div className="table-wrap"><table><thead><tr><th>Description</th><th>Source</th><th>Date</th><th>Amount</th><th/></tr></thead><tbody>{rows.map(r=><tr key={r.id}><td><b>{r.description}</b></td><td><span className="tag green-tag">{r.source}</span></td><td>{r.income_date}</td><td className="amount positive">{money(r.amount)}</td><td><div className="row-actions"><button onClick={()=>onEdit(r)}><Pencil size={15}/></button><button onClick={()=>onDelete(r.id)}><Trash2 size={15}/></button></div></td></tr>)}</tbody></table>{!rows.length&&<Empty text="No matching income records found."/>}</div>}
function Analytics({monthly,categories,month}:{monthly:any[];categories:any[];month:string}){return <div className="dashboard-grid analytics-grid"><div className="panel chart-panel"><PanelHead title="Monthly cash flow" subtitle={`Income and expenses in ${month.slice(0,4)}`}/><div className="chart tall"><ResponsiveContainer width="100%" height="100%"><BarChart data={monthly}><CartesianGrid strokeDasharray="3 3" vertical={false}/><XAxis dataKey="month" tickFormatter={(v)=>v.slice(5)}/><YAxis/><Tooltip formatter={(v:any)=>money(Number(v))}/><Legend/><Bar dataKey="income" fill="#18b889" radius={[5,5,0,0]}/><Bar dataKey="expenses" fill="#f17c83" radius={[5,5,0,0]}/></BarChart></ResponsiveContainer></div></div><div className="panel"><PanelHead title="Spending by category" subtitle={`Expense distribution for ${month}`}/>{categories.length?<><div className="chart pie"><ResponsiveContainer width="100%" height="100%"><PieChart><Pie data={categories} dataKey="amount" nameKey="category" innerRadius={58} outerRadius={90} paddingAngle={3}>{categories.map((_:any,i:number)=><Cell key={i} fill={palette[i%palette.length]}/>)}</Pie><Tooltip formatter={(v:any)=>money(Number(v))}/></PieChart></ResponsiveContainer></div>{categories.map((c:any,i:number)=><div className="legend-row" key={c.category}><span style={{background:palette[i%palette.length]}}/>{c.category}<b>{money(c.amount)}</b></div>)}</>:<Empty text="No expense data for this month."/>}</div></div>}
function ReportMetric({label,value}:{label:string;value:string}){return <div className="report-metric"><small>{label}</small><b>{value}</b></div>}
function downloadReport(report:any){if(!report)return;const rows=[['Type','Description','Category/Source','Date','Amount'],...(report.income||[]).map((x:any)=>['Income',x.description,x.source,x.date,x.amount]),...(report.expenses||[]).map((x:any)=>['Expense',x.description,x.category,x.date,x.amount])];const csv=rows.map(r=>r.map(v=>`"${String(v??'').replaceAll('"','""')}"`).join(',')).join('\n');const url=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));const a=document.createElement('a');a.href=url;a.download='paisaflow-report.csv';a.click();URL.revokeObjectURL(url)}
function RecordModal({kind,initial,categories,month,onClose,onSave}:{kind:'expense'|'income'|'category'|'budget';initial:any;categories:Category[];month:string;onClose:()=>void;onSave:(p:any)=>void}){const [description,setDescription]=useState(initial?.description||'');const [amount,setAmount]=useState(initial?.amount?.toString()||'');const [category,setCategory]=useState(initial?.category||'');const [source,setSource]=useState(initial?.source||'');const [date,setDate]=useState(initial?.expense_date||initial?.income_date||today());const [name,setName]=useState(initial?.name||'');const [kindValue,setKindValue]=useState(initial?.kind||'expense');const [color,setColor]=useState(initial?.color||'#64748b');const [budgetMonth,setBudgetMonth]=useState(initial?.month||month);const [formError,setFormError]=useState('');const title=initial?'Edit ': 'Add ';const label=kind==='expense'?'Expense':kind==='income'?'Income':kind==='category'?'Category':'Budget';function submit(e:FormEvent){e.preventDefault();setFormError('');if(kind==='expense'||kind==='income'){const value=Number(amount);if(!description.trim()||!Number.isFinite(value)||value<=0||!date){setFormError('Enter a description, positive amount and valid date.');return}onSave(kind==='expense'?{description,amount:value,category:category.trim(),expense_date:date}:{description,amount:value,source:source.trim(),income_date:date})}else if(kind==='category'){if(!name.trim()){setFormError('Enter a category name.');return}onSave({name,kind:kindValue,color})}else{const value=Number(amount);if(!category.trim()||!Number.isFinite(value)||value<=0){setFormError('Enter a category and positive budget amount.');return}onSave({category,month:budgetMonth,amount:value})}}return <div className="modal-backdrop" onMouseDown={e=>{if(e.target===e.currentTarget)onClose()}}><form className="modal" onSubmit={submit}><div className="modal-head"><div><span className="eyebrow">PAISAFLOW</span><h2>{title}{label}</h2></div><button type="button" className="icon-button" onClick={onClose}><X/></button></div>{(kind==='expense'||kind==='income')&&<><label>Description<input autoFocus value={description} onChange={e=>setDescription(e.target.value)} placeholder="e.g. Monthly rent" required/></label><label>{kind==='expense'?'Category':'Income source'}<input list="category-options" value={kind==='expense'?category:source} onChange={e=>kind==='expense'?setCategory(e.target.value):setSource(e.target.value)} placeholder={kind==='expense'?'e.g. Housing':'e.g. Salary'} required/><datalist id="category-options">{categories.filter(c=>c.kind===kind||c.kind==='both').map(c=><option key={c.id} value={c.name}/>)}</datalist></label><div className="form-two"><label>Amount (₹)<input type="number" min="0.01" step="0.01" value={amount} onChange={e=>setAmount(e.target.value)} required/></label><label>Date<input type="date" value={date} onChange={e=>setDate(e.target.value)} required/></label></div></>}{kind==='category'&&<><label>Category name<input autoFocus value={name} onChange={e=>setName(e.target.value)} required/></label><label>Applies to<select value={kindValue} onChange={e=>setKindValue(e.target.value as any)}><option value="expense">Expenses</option><option value="income">Income</option><option value="both">Both</option></select></label><label>Color<input type="color" value={color} onChange={e=>setColor(e.target.value)}/></label></>}{kind==='budget'&&<><label>Expense category<input list="budget-category-options" value={category} onChange={e=>setCategory(e.target.value)} required/><datalist id="budget-category-options">{categories.filter(c=>c.kind==='expense'||c.kind==='both').map(c=><option key={c.id} value={c.name}/>)}</datalist></label><div className="form-two"><label>Monthly limit (₹)<input type="number" min="0.01" step="0.01" value={amount} onChange={e=>setAmount(e.target.value)} required/></label><label>Month<input type="month" value={budgetMonth} onChange={e=>setBudgetMonth(e.target.value)} required/></label></div></>}{formError&&<div className="form-error">{formError}</div>}<div className="modal-actions"><button type="button" className="secondary-button" onClick={onClose}>Cancel</button><button className="primary-button" type="submit">Save {label.toLowerCase()}</button></div></form></div>}
