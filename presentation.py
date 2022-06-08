import streamlit as st

from datetime import datetime, timedelta
import token_manager
import requests
import json
import os
import re

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
from matplotlib.cbook import get_sample_data
import matplotlib.image as mpimg
import pandas as pd
import numpy as np
import seaborn as sns

# Color Pallette
color1 = '#10120F'
color2 = '#989997'
color3 = '#FD422B'
color4 = '#419279'
color5 = '#F4F3F3'

# Fontsize
h1 = 24
h2 = 20
h3 = 16

fontname = 'Courier New'

lst_of_brokers = ['297 Properties',
 'Able Realty Aruba',
 'Absolute Real Estate',
 'Alto Vista Real Estate',
 'Aruba Brokers Real Estate',
 'Aruba Happy Realty',
 'Aruba Home Finders',
 'Aruba Living Today',
 'Aruba Palms Realtors',
 'Aruba Real Estate Brokers',
 'Aruba Top Homes Real Estate',
 'Associated Realtors Aruba',
 'Ben Real Estate Services',
 'Best Buy Realty Aruba',
 'Bon Choice Aruba Realty',
 'CLW Real Estate',
 'Capital Reliance Real Estate',
 'Casnan.com Aruba Real Estate',
 'Century 21 Aruba Real Estate',
 'Clearly Realty',
 'Coldwell Banker Aruba Realty',
 "Edith's Aruba Real Estate Solutions",
 'Ford Property Aruba',
 'Homecity Aruba Real Estate',
 'Homes by Jenn Aruba Real Estate',
 'James Edition',
 'Keller Williams Real Estate Aruba',
 'MPG Real Estate',
 'Maurer Real Estate',
 'Prima Casa Real Estate',
 'R4 Real Estate',
 'Remax Advantage Realty',
 'Rent House Aruba',
 'Smiley Aruba',
 'Solito Trust & Management',
 "Sotheby's International Realty Aruba",
 'Spazio Realty',
 'Strategic Asset Management',
 'Sun Caribbean Realty',
 'T&T Real Estate']

st.markdown(
"""
<style type="text/css">
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

#outlook a {
  padding: 0;
}

.es-button {
  mso-style-priority: 100 !important;
  text-decoration: none !important;
}

a[x-apple-data-detectors] {
  color: inherit !important;
  text-decoration: none !important;
  font-size: inherit !important;
  font-family: inherit !important;
  font-weight: inherit !important;
  line-height: inherit !important;
}

.es-desk-hidden {
  display: none;
  float: left;
  overflow: hidden;
  width: 0;
  max-height: 0;
  line-height: 0;
  mso-hide: all;
}

[data-ogsb] .es-button {
  border-width: 0 !important;
  padding: 10px 20px 10px 20px !important;
}

[data-ogsb] .es-button.es-button-1 {
  padding: 10px 20px !important;
}

@media only screen and (max-width:600px) {

  p,
  ul li,
  ol li,
  a {
    line-height: 150% !important
  }

  h1 {
    font-size: 30px !important;
    text-align: center;
    line-height: 120% !important
  }

  h2 {
    font-size: 26px !important;
    text-align: center;
    line-height: 120% !important
  }

  h3 {
    font-size: 20px !important;
    text-align: center;
    line-height: 120% !important
  }

  .es-header-body h1 a,
  .es-content-body h1 a,
  .es-footer-body h1 a {
    font-size: 30px !important
  }

  .es-header-body h2 a,
  .es-content-body h2 a,
  .es-footer-body h2 a {
    font-size: 26px !important
  }

  .es-header-body h3 a,
  .es-content-body h3 a,
  .es-footer-body h3 a {
    font-size: 20px !important
  }

  .es-menu td a {
    font-size: 16px !important
  }

  .es-header-body p,
  .es-header-body ul li,
  .es-header-body ol li,
  .es-header-body a {
    font-size: 16px !important
  }

  .es-content-body p,
  .es-content-body ul li,
  .es-content-body ol li,
  .es-content-body a {
    font-size: 16px !important
  }

  .es-footer-body p,
  .es-footer-body ul li,
  .es-footer-body ol li,
  .es-footer-body a {
    font-size: 16px !important
  }

  .es-infoblock p,
  .es-infoblock ul li,
  .es-infoblock ol li,
  .es-infoblock a {
    font-size: 12px !important
  }

  *[class="gmail-fix"] {
    display: none !important
  }

  .es-m-txt-c,
  .es-m-txt-c h1,
  .es-m-txt-c h2,
  .es-m-txt-c h3 {
    text-align: center !important
  }

  .es-m-txt-r,
  .es-m-txt-r h1,
  .es-m-txt-r h2,
  .es-m-txt-r h3 {
    text-align: right !important
  }

  .es-m-txt-l,
  .es-m-txt-l h1,
  .es-m-txt-l h2,
  .es-m-txt-l h3 {
    text-align: left !important
  }

  .es-m-txt-r img,
  .es-m-txt-c img,
  .es-m-txt-l img {
    display: inline !important
  }

  .es-button-border {
    display: block !important
  }

  .es-adaptive table,
  .es-left,
  .es-right {
    width: 100% !important
  }

  .es-content table,
  .es-header table,
  .es-footer table,
  .es-content,
  .es-footer,
  .es-header {
    width: 100% !important;
    max-width: 600px !important
  }

  .es-adapt-td {
    display: block !important;
    width: 100% !important
  }

  .adapt-img {
    width: 100% !important;
    height: auto !important
  }

  .es-m-p0 {
    padding: 0px !important
  }

  .es-m-p0r {
    padding-right: 0px !important
  }

  .es-m-p0l {
    padding-left: 0px !important
  }

  .es-m-p0t {
    padding-top: 0px !important
  }

  .es-m-p0b {
    padding-bottom: 0 !important
  }

  .es-m-p20b {
    padding-bottom: 20px !important
  }

  .es-mobile-hidden,
  .es-hidden {
    display: none !important
  }

  tr.es-desk-hidden,
  td.es-desk-hidden,
  table.es-desk-hidden {
    width: auto !important;
    overflow: visible !important;
    float: none !important;
    max-height: inherit !important;
    line-height: inherit !important
  }

  tr.es-desk-hidden {
    display: table-row !important
  }

  table.es-desk-hidden {
    display: table !important
  }

  td.es-desk-menu-hidden {
    display: table-cell !important
  }

  .es-menu td {
    width: 1% !important
  }

  table.es-table-not-adapt,
  .esd-block-html table {
    width: auto !important
  }

  table.es-social {
    display: inline-block !important
  }

  table.es-social td {
    display: inline-block !important
  }

  a.es-button,
  button.es-button {
    font-size: 20px !important;
    display: block !important;
    border-width: 10px 0px 10px 0px !important
  }
}


</style>
""", unsafe_allow_html=True)

# header {visibility: hidden;}
#

filters = {
    'house': 'build_up_m2',
    'land': 'lot_size_m2',
    'condominium': 'build_up_m2'
}

# ---------------------------------------------------------------------------- #

@st.cache
def get_data(filename='presentation.csv') -> pd.DataFrame:

    df = pd.read_csv(filename)
    df.columns = ['address', 'bathrooms', 'bedrooms', 'build_up_m2', 'contract', 'date_posted', 'district', 'location', 'lot_size_m2', 'Rights to land', 'pool', 'property_type', 'price']
    return df

# ---------------------------------------------------------------------------- #

def remove_outliers(df, cols):

    # Compute Quartiles and IQR
    for col in cols:
        q1 = np.nanpercentile(df[col].values, 25)
        q3 = np.nanpercentile(df[col].values, 75)
        iqr = q3 - q1
        ll = q1 - 1.5 * iqr
        ul = q3 + 1.5 * iqr

        # Subset by limits
        df = df[df[col] >= ll]
        df = df[df[col]  < ul]

    return df

# ---------------------------------------------------------------------------- #

def select_data(df, property_type):
    # Filter for Land properties
    df = df[(df.property_type == property_type) & (df.contract == 'sale')]

    # Filter out properties where build/lot size is 0
    if property_type != 'land':
        df = df[(df['build_up_m2'] != 0) & (df['lot_size_m2'] != 0)]

        # Compute price per square meter
        df['price_per_m2_build'] = df.price / df.build_up_m2
        df['price_per_m2_lot'] = df.price / df.lot_size_m2

        # Remove outlier observations
        df = remove_outliers(df, ['price', 'bedrooms', 'bathrooms', 'build_up_m2', 'lot_size_m2', 'price_per_m2_build', 'price_per_m2_lot'])

        return df[['date_posted', 'district', 'Rights to land', 'bedrooms', 'bathrooms', 'build_up_m2', 'lot_size_m2', 'price_per_m2_build', 'price_per_m2_lot']]

    else:
        df = df[df['lot_size_m2'] != 0]

        # Compute price per square meter
        df['price_per_m2_lot'] = df.price / df.lot_size_m2

        # Remove outlier observations
        df = remove_outliers(df, ['price', 'lot_size_m2', 'price_per_m2_lot'])

        return df[['date_posted', 'district', 'Rights to land', 'lot_size_m2', 'price_per_m2_lot']]

# ---------------------------------------------------------------------------- #

def plot(df1, df2, property_type):
    fig , axes = plt.subplots(1, 2, sharey=True, sharex=True, figsize=(16, 8))

    if property_type != 'land':
        sns.histplot(data=df1,
                     x='price_per_m2_build',
                     kde=True,
                     # palette=[color3, color4],
                     hue='Rights to land',
                     legend=False,
                     palette=[color3, color4],
                     edgecolor=color1,
                     ax=axes[0],
                     bins=20)

        sns.histplot(data=df2,
                     x='price_per_m2_build',
                     kde=True,
                     # palette=[color3, color4],
                     hue='Rights to land',
                     legend=True,
                     palette=[color3, color4],
                     edgecolor=color1,
                     ax=axes[1],
                     bins=20,
                     label='Rights to land')

    else:
        sns.histplot(data=df1,
                     x='price_per_m2_lot',
                     kde=True,
                     # palette=[color3, color4],
                     hue='Rights to land',
                     legend=False,
                     palette=[color3, color4],
                     edgecolor=color1,
                     ax=axes[0],
                     bins=20)

        sns.histplot(data=df2,
                     x='price_per_m2_lot',
                     kde=True,
                     # palette=[color3, color4],
                     hue='Rights to land',
                     legend=True,
                     palette=[color3, color4],
                     edgecolor=color1,
                     ax=axes[1],
                     bins=20,
                     label='Rights to land')

    # Titles
    fig.suptitle(f'Distribution {property_type.title()} Asking Price',
                 fontsize=h1,
                 fontweight='bold',
                 y=1.05,
                 x=0.125,
                 ha='left',
                 fontname=fontname
                )

    axes[0].set_title(f"AWG ({filters[property_type]})",
                 fontdict={
                     'fontsize': h2,
                     'verticalalignment': 'baseline',
                     'horizontalalignment': 'left'
                 },
                 loc='left',
                 fontname=fontname,
                 pad=50
                )

    # Set Grid lines
    axes[0].yaxis.grid(linestyle='--')
    axes[1].yaxis.grid(linestyle='--')

    # Set Fontsize Labels
    axes[0].tick_params(labelsize=h3)
    # axes[0].tick_params('x',  rotation=20)

    axes[1].tick_params(labelsize=h3)
    # axes[1].tick_params('x',  rotation=20)

    # Hide Spines
    axes[0].spines['right'].set_visible(False)
    axes[0].spines['top'].set_visible(False)
    # axes[0].spines['left'].set_visible(False)

    axes[1].spines['right'].set_visible(False)
    axes[1].spines['top'].set_visible(False)
    axes[1].spines['left'].set_visible(False)


    if property_type == 'land':
        xticks = axes[0].get_xticks()
        axes[0].set_xticklabels([f"{i:,.0f}" for i in xticks])

        xticks = axes[1].get_xticks()
        axes[1].set_xticklabels([f"{i:,.0f}" for i in xticks])

    else:
        xticks = axes[0].get_xticks()
        axes[0].set_xticklabels([f"{i/1_000:,.0f}k" for i in xticks])

        xticks = axes[1].get_xticks()
        axes[1].set_xticklabels([f"{i/1_000:,.0f}k" for i in xticks])

    # Source
    axes[0].set_xlabel("\n2020",
                 fontsize=h3,
                 loc='center',
                 color=color1,
    #              fontstyle='italic',
                 )

    axes[1].set_xlabel("\n2021",
                 fontsize=h3,
                 loc='center',
                 color=color1,
    #              fontstyle='italic',
                 )

    axes[0].set_ylabel("Count",
                 fontsize=h3,
                 color=color1,
                 )

    plt.setp(axes[1].get_legend().get_texts(), fontsize=h2)
    plt.setp(axes[1].get_legend().get_title(), fontsize=h2)

    # save image
    # Save graph as PNG
    filename = 'histplot.png'
    fig.savefig(filename, dpi=500, format='png', bbox_inches='tight', facecolor=fig.get_facecolor())

    return fig

# ---------------------------------------------------------------------------- #

def boxplot(df, property_type, year):

    fig, ax = plt.subplots(figsize=(16, 8))

    if property_type != 'land':
        sns.boxplot(data=df,
                    x='district',
                    y='price_per_m2_build',
                    hue='Rights to land',
                    order=['Noord/Tanki Leendert', 'Paradera', 'Oranjestad West', 'Oranjestad Oost', 'Santa Cruz', 'Savaneta', 'San Nicolas Noord', 'San Nicolas Zuid'],
                    palette=[color2, color5],
                    dodge=True,
                    medianprops={'color': color3, 'linewidth': 2},
                    ax=ax, boxprops={'alpha': .5})

        ax.hlines(df_2020['price_per_m2_build'].median(), -.5, 7.5, color=color4, label='median', linewidth=2)

    else:
        sns.boxplot(data=df[df['Rights to land'] == 'freehold'],
                    x='district',
                    y='price_per_m2_lot',
                    # hue='Rights to land',
                    order=['Noord/Tanki Leendert', 'Paradera', 'Oranjestad West', 'Oranjestad Oost', 'Santa Cruz', 'Savaneta', 'San Nicolas Noord', 'San Nicolas Zuid'],
                    palette=[color2],
                    dodge=True,
                    medianprops={'color': color3, 'linewidth': 2},
                    ax=ax, boxprops={'alpha': .5})

        ax.hlines(df_2020['price_per_m2_lot'].median(), -.5, 7.5, color=color4, label='median', linewidth=2)

    # Titles
    fig.suptitle(f'{property_type.title()} For Sale, Asking Price Distribution {year}',
                 fontsize=h1,
                 fontweight='bold',
                 y=1.05,
                 x=0.125,
                 ha='left',
                 fontname=fontname
                )

    ax.set_title(f"in AWG ({filters[property_type]})",
                 fontdict={
                     'fontsize': h2,
                     'verticalalignment': 'baseline',
                     'horizontalalignment': 'left'
                 },
                 loc='left',
                 pad=50,
                 fontname=fontname
                )

    # Set Grid lines
    ax.yaxis.grid(linestyle='--')

    # Set Fontsize Labels
    ax.tick_params(labelsize=h3)
    ax.tick_params('x',  rotation=20)

    # Hide Spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # format y-ticks
    if property_type == 'land':
        yticks = ax.get_yticks()
        ax.set_yticklabels([f"{i:,.0f}" for i in yticks])

        yticks = ax.get_yticks()
        ax.set_yticklabels([f"{i:,.0f}" for i in yticks])

    else:
        yticks = ax.get_yticks()
        ax.set_yticklabels([f"{i/1_000:,.1f}k" for i in yticks])

        yticks = ax.get_yticks()
        ax.set_yticklabels([f"{i/1_000:,.1f}k" for i in yticks])

    # Source
    ax.set_xlabel("",
                 fontsize=h3,
                 loc='left',
                 color=color2,
                 fontstyle='italic',
                 )


    ax.set_ylabel('')
    ax.legend(fontsize=h3)

    return fig

# ---------------------------------------------------------------------------- #
property_type = st.sidebar.selectbox('Choose property type', options=['house', 'land'])

df_origin = get_data()

df = select_data(df_origin, property_type)


# ---------------------------------------------------------------------------- #
# Display
# st.write(df.columns)


df_2020 = df[(df.date_posted >= '2020-04-17') & (df.date_posted < '2021-04-16')]
df_2021 = df[(df.date_posted >= '2021-04-17') & (df.date_posted < '2022-04-16')]


st.markdown(
"""
<table width="100%" cellspacing="0" cellpadding="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;border:none;">
  <tbody>
    <tr style="border:none;">
      <td valign="top" align="center" style="padding:0;Margin:0;width:560px;border:none;">
        <table width="100%" cellspacing="0" cellpadding="0" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;border:none;">
          <tbody>
            <tr style="border:none;">
              <td style="Margin:0;padding-bottom:5px;padding-top:40px;padding-left:40px;padding-right:40px;font-size:0px;border:none;" align="center"><img
                  src="https://ci5.googleusercontent.com/proxy/NYKYbVYILpgEKj2U-RLRi44JB6Lua6Mp3xl52zVoIXxRj79rHn2eOSCXfpF4BSmkzsNR-yr0RLXjeEeGrzmtjYtiFFAvewmHcCvP6VoOcStiN3D78Ph_kidGzWov2msp8Olktp2mlCEYWVxi9H0HwhqnL8I3e6C8cYFWSqBDoGZHyVhNiQ=s0-d-e1-ft#https://nznsml.stripocdn.email/content/guids/CABINET_526f2a71e5569e068dd8041c7a90a257/images/47091613938488738.png"
                  alt="" width="160" style="display:block;border:0px;outline:none;margin: auto;" class="CToWUd"></td>
            </tr>
            <tr style="border:none">
              <td align="center" style="padding:0;Margin:0;border:none;">
                <p
                  style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;line-height:21px;color:#333333;font-size:14px">
                  <i>T</i><i>he new standard in&nbsp;</i><i>Aruba real estate.</i><br>
                </p>
              </td>
            </tr>
          </tbody>
        </table>
      </td>
    </tr>
  </tbody>
</table>
""", unsafe_allow_html=True)


# Section 1
# ---------------------------------------------------------------------------- #
st.header("Mercala", anchor='section-1')

st.markdown(
"""
#### What is Mercala?
Mercala is a cloud-based service application that provides its users with
real-time updates on local real estate listings.
""")

st.markdown(
"""#### How does it work?
Mercala deploys proprietary algorithms to collected data across numerous
local broker sites and stores it in a central database.
""")

st.markdown(
"""
#### When did *this* happen?
Mercala started as a humble exchange of CSV files through e-mail at the beginning
of 2020. Shortly after on April 17th, 2020 Mercala.org was launched to the public.
""")

st.markdown(
"""
#### Where can you find Mercala?
You can sign up at https://mercala.org for a 3-day free trail.
\ne-mail: info@mercala.org
""")

st.markdown(
"""
#### Who is behind Mercala?
Creator and founder Angelo J. Willems
\nFull-stack developer Jonathan van Putten
""")

st.subheader("List of Brokers", anchor='section-1.1')
with st.expander(' '):
    cols = st.columns(2)
    for index, broker in enumerate(lst_of_brokers[:20]):
        cols[0].write(f"{index + 1})     {broker}")

    for index, broker in enumerate(lst_of_brokers[20:]):
        cols[1].write(f"{index + 21})     {broker}")



# Section 2
# ---------------------------------------------------------------------------- #
st.subheader('Summary Statistics', anchor='section-2')
cols = st.columns(2)
cols[0].write(f'{property_type.title()} For Sale 2020')
cols[0].write(df_2020.describe().style.format('{:,.0f}'))
cols[1].write(f'{property_type.title()} For Sale 2021')
cols[1].write(df_2021.describe().style.format('{:,.0f}'))


# st.header("Trends", anchor='section-2')
st.pyplot(plot(df_2020, df_2021, property_type))

st.header('Indicators')
st.subheader('Isolating Land prices from House prices')
st.write('Median asking price per m2 of land (including house): 898')
st.write('Median asking price per m2 of land (excluding house): 288')
st.write('Median lot size: 600 m2')
st.write('Median build up: 180 m2')
st.write('Median asking price per m2 of land (excluding land): (898 - 288) x 600 / 180 = 2,033')




# Section 3
# ---------------------------------------------------------------------------- #
st.header("Trends", anchor='section-3')
st.pyplot(boxplot(df_2020, property_type, '2020'))
st.pyplot(boxplot(df_2021, property_type, '2021'))

# district = st.sidebar.selectbox('Choose district', options=['Noord/Tanki Leendert', 'Paradera', 'Oranjestad West', 'Oranjestad Oost', 'Santa Cruz', 'Savaneta', 'San Nicolas Noord', 'San Nicolas Zuid'])



st.subheader('Asking Price Change')
for district in ['Noord/Tanki Leendert', 'Paradera', 'Oranjestad West', 'Oranjestad Oost', 'Santa Cruz', 'Savaneta', 'San Nicolas Noord', 'San Nicolas Zuid']:
    cols = st.columns(3)
    cols[0].write(district);
    cols[1].metric('2021', f"{df_2021[df_2021.district == district].median()['price_per_m2_lot']:,.0f}", delta=f"{(df_2021[df_2021.district == district].median()['price_per_m2_lot']/df_2020[df_2020.district == district].median()['price_per_m2_lot']-1)*100:,.1f}%")
    cols[2].metric('2020', f"{df_2020[df_2020.district == district].median()['price_per_m2_lot']:,.0f}")
# ---------------------------------------------------------------------------- #
# SIDEBAR
st.sidebar.markdown("[Mercala](#section-1)", unsafe_allow_html=True)
st.sidebar.markdown("[Summary Statistics](#section-2)", unsafe_allow_html=True)
st.sidebar.markdown("[Opportunities](#section-2)", unsafe_allow_html=True)

# toc.generate()
