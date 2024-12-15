import streamlit as st
import numpy as np
import altair as alt
import pandas as pd

st.set_page_config(page_title="Υπόδειγμα Solow ", layout="centered")

st.title("Διαδραστική Εξερεύνηση του Υποδείγματος Solow")

# Εισαγωγή
st.write("""
Το υπόδειγμα Solow αναλύει τη μακροχρόνια οικονομική ανάπτυξη με βάση τη συσσώρευση κεφαλαίου, 
τον ρυθμό αύξησης πληθυσμού, την αποταμίευση, την απόσβεση και (προαιρετικά) την τεχνολογική πρόοδο.

Χρησιμοποιούμε μία Cobb-Douglas συνάρτηση παραγωγής:
""")
st.latex(r"y = k^{\alpha}")

st.write("""
όπου \(y\) η παραγωγή ανά εργαζόμενο, \(k\) το κεφάλαιο ανά εργαζόμενο, \( \alpha \) το μερίδιο του κεφαλαίου. 
Ο λόγος αποταμίευσης \(s\) καθορίζει την επένδυση \(i = s y\).  
Η απόσβεση έχει ρυθμό \(\delta\), ο πληθυσμός αυξάνεται με \(n\) και, αν υπάρχει, η τεχνολογική πρόοδος εξελίσσεται με \(g\).

Σε μακροχρόνια ισορροπία (steady state), το κεφάλαιο ανά εργαζόμενο σταθεροποιείται.
""")

# Sidebar παράμετροι
st.sidebar.header("Παράμετροι Μοντέλου")
alpha = st.sidebar.slider("Μερίδιο Κεφαλαίου (α)", 0.1, 0.9, 0.3, 0.01)
s = st.sidebar.slider("Λόγος Αποταμίευσης (s)", 0.01, 0.9, 0.2, 0.01)
delta = st.sidebar.slider("Ρυθμός Απόσβεσης (δ)", 0.01, 0.2, 0.05, 0.01)
n = st.sidebar.slider("Ρυθμός Αύξησης Πληθυσμού (n)", 0.0, 0.05, 0.01, 0.001)
g = st.sidebar.slider("Ρυθμός Τεχνολογικής Προόδου (g)", 0.0, 0.05, 0.01, 0.001)
k0 = st.sidebar.slider("Αρχικό Κεφάλαιο ανά Εργαζόμενο (k₀)", 0.1, 50.0, 10.0, 0.5)

# Υπολογισμός Steady State (g=0)
st.write("### Steady State:")
k_star = (s/(n+delta))**(1/(1-alpha))
y_star = k_star**alpha
c_star = (1 - s)*y_star
st.latex(r"k^* = \left(\frac{s}{n+\delta}\right)^{\frac{1}{1-\alpha}} = " + f"{k_star:.4f}")
st.latex(r"y^* = (k^*)^{\alpha} = " + f"{y_star:.4f}")
st.latex(r"c^* = (1 - s)y^* = " + f"{c_star:.4f}")

# Steady State με τεχνολογική πρόοδο
if g > 0:
    k_tilde_star = (s/(n+delta+g))**(1/(1-alpha))
    y_tilde_star = k_tilde_star**alpha
    c_tilde_star = (1-s)*y_tilde_star
    st.write("**Με Τεχνολογική Πρόοδο (g>0):**")
    st.latex(r"\tilde{k}^* = \left(\frac{s}{n+\delta+g}\right)^{\frac{1}{1-\alpha}} = " + f"{k_tilde_star:.4f}")
    st.latex(r"\tilde{y}^* = (\tilde{k}^*)^{\alpha} = " + f"{y_tilde_star:.4f}")
    st.latex(r"\tilde{c}^* = (1 - s)\tilde{y}^* = " + f"{c_tilde_star:.4f}")

st.write("""
Χωρίς τεχνολογική πρόοδο, τα k*, y*, c* είναι σταθερά μακροχρόνια.  
Με τεχνολογική πρόοδο, σταθεροποιούνται οι ανά **αποτελεσματικό** εργαζόμενο ποσότητες, 
ενώ η πραγματική παραγωγή ανά εργαζόμενο αυξάνεται με το χρόνο.
""")

# Golden Rule
st.write("### Golden Rule Επίπεδο Κεφαλαίου:")
k_gr = (alpha/(n+delta))**(1/(1-alpha))
y_gr = k_gr**alpha
c_gr = y_gr - (n+delta)*k_gr
st.latex(r"\text{Golden Rule: } f'(k_{GR})=n+\delta")
st.latex(r"k_{GR} = \left(\frac{\alpha}{n+\delta}\right)^{\frac{1}{1-\alpha}} = " + f"{k_gr:.4f}")
st.latex(r"y_{GR} = (k_{GR})^{\alpha} = " + f"{y_gr:.4f}")
st.latex(r"c_{GR} = y_{GR} - (n+\delta)k_{GR} = " + f"{c_gr:.4f}")

st.write("Το Golden Rule μεγιστοποιεί τη σταθεροποιημένη κατανάλωση.")

# Δυναμική Προσομοίωση
st.write("### Δυναμική Προσομοίωση:")
T=200
k_level=np.zeros(T)
k_level[0]=k0
y_level=np.zeros(T)
y_level[0]=k_level[0]**alpha
c_level=np.zeros(T)
c_level[0]=(1 - s)*y_level[0]

if g>0:
    A=np.zeros(T)
    A[0]=1.0
    k_tilde=np.zeros(T)
    k_tilde[0]=k_level[0]
    y_tilde=np.zeros(T)
    y_tilde[0]=k_tilde[0]**alpha
    c_tilde=np.zeros(T)
    c_tilde[0]=(1 - s)*y_tilde[0]

for t in range(1,T):
    if g>0:
        A[t]=A[t-1]*(1+g)
        k_tilde[t]=(s*(k_tilde[t-1]**alpha)+(1-delta)*k_tilde[t-1])/((1+n)*(1+g))
        k_level[t]=k_tilde[t]*A[t]
        y_level[t]=k_level[t]**alpha
        y_tilde[t]=k_tilde[t]**alpha
        c_level[t]=(1 - s)*y_level[t]
        c_tilde[t]=(1 - s)*y_tilde[t]
    else:
        k_level[t]=(s*(k_level[t-1]**alpha)+(1-delta)*k_level[t-1])/(1+n)
        y_level[t]=k_level[t]**alpha
        c_level[t]=(1-s)*y_level[t]

data_sim=[]
for t in range(T):
    data_sim.append({"t":t,"variable":"k","value":k_level[t]})
    data_sim.append({"t":t,"variable":"y","value":y_level[t]})
    data_sim.append({"t":t,"variable":"c","value":c_level[t]})
    if g>0:
        data_sim.append({"t":t,"variable":"k~","value":k_tilde[t]})
        data_sim.append({"t":t,"variable":"y~","value":y_tilde[t]})
        data_sim.append({"t":t,"variable":"c~","value":c_tilde[t]})

df_sim=pd.DataFrame(data_sim)
chart_sim=alt.Chart(df_sim).mark_line().encode(
    x='t:Q',
    y='value:Q',
    color='variable:N'
).properties(width=700, height=300, title="Εξέλιξη μεταβλητών με τον χρόνο")
st.altair_chart(chart_sim, use_container_width=True)

st.write("""
Όταν \(g=0\), οι μεταβλητές ανά εργαζόμενο συγκλίνουν σε steady state.  
Όταν \(g>0\), οι ανά αποτελεσματικό εργαζόμενο ποσότητες σταθεροποιούνται, 
ενώ η παραγωγή ανά εργαζόμενο αυξάνεται διαχρονικά.
""")

# Διάγραμμα Φάσης χωρίς τεχνολογία
st.write("### Διάγραμμα Φάσης (g=0):")
k_range=np.linspace(0.001,max(k_star*2,k0*2,50),200)
investment = s*k_range**alpha
break_even = (n+delta)*k_range

data_phase=[]
for val in k_range:
    data_phase.append({"k":val,"value":s*(val**alpha),"type":"Επένδυση (s k^{\alpha})"})
    data_phase.append({"k":val,"value":(n+delta)*val,"type":"Break-even ((n+δ)k)"})

df_phase=pd.DataFrame(data_phase)
phase_chart=alt.Chart(df_phase).mark_line().encode(
    x=alt.X('k:Q', title='k'),
    y=alt.Y('value:Q', title='Επένδυση / Break-even'),
    color='type:N'
).properties(width=700, height=300, title="Διάγραμμα Φάσης (g=0)")

phase_line=alt.Chart(pd.DataFrame({'k':[k_star]})).mark_rule(color='red').encode(x='k:Q')
st.altair_chart(phase_chart+phase_line, use_container_width=True)
st.write(fr"Η κόκκινη γραμμή στο k = {k_star:.4f} δείχνει το steady state χωρίς τεχνολογική πρόοδο.")

# Διάγραμμα Φάσης με τεχνολογία
st.write("### Διάγραμμα Φάσης (g>0):")
if g>0:
    k_tilde_range = np.linspace(0.001, max((k_tilde_star*2 if k_tilde_star else 50),50),200)
    invest_tilde = s*(k_tilde_range**alpha)
    break_even_tilde=(n+delta+g)*k_tilde_range

    data_phase_tilde=[]
    for val in k_tilde_range:
        data_phase_tilde.append({"k_tilde":val,"value":s*(val**alpha),"type":"Επένδυση (s (k~)^{\alpha})"})
        data_phase_tilde.append({"k_tilde":val,"value":(n+delta+g)*val,"type":"Break-even ((n+δ+g)k~)"})

    df_phase_tilde = pd.DataFrame(data_phase_tilde)
    phase_tilde_chart = alt.Chart(df_phase_tilde).mark_line().encode(
        x=alt.X('k_tilde:Q', title='k~'),
        y=alt.Y('value:Q', title='Επένδυση / Break-even'),
        color='type:N'
    ).properties(width=700, height=300, title="Διάγραμμα Φάσης (g>0)")

    phase_tilde_line = alt.Chart(pd.DataFrame({'k_tilde':[k_tilde_star]})).mark_rule(color='red').encode(x='k_tilde:Q')
    st.altair_chart(phase_tilde_chart+phase_tilde_line, use_container_width=True)
    st.write(fr"Στο k~ = {k_tilde_star:.4f} η οικονομία σταθεροποιείται (ανά αποτελεσματικό εργαζόμενο).")
else:
    st.write("Ορίστε g>0 για να δείτε το διάγραμμα φάσης με τεχνολογική πρόοδο.")


st.write("""
Πειραματιστείτε με τις παραμέτρους για να δείτε πώς αλλάζει το steady state και η δυναμική σύγκλισης.
""")
