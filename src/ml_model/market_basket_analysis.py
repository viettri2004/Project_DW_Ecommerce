import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from sqlalchemy import create_engine
import os

DB_URL = "postgresql+psycopg2://postgres:130604@127.0.0.1:5432/ecommerce_dw" 
engine = create_engine(DB_URL)

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..', '..')
OUTPUT_RULES_PATH = os.path.join(project_root, 'src', 'ml_model', 'output_rules.csv')

def prepare_mba_input(engine):
    """
    1. Truy vấn dữ liệu cần thiết (invoiceno, description) từ DW.
    2. Chuyển đổi thành định dạng One-Hot Encoded.
    """
    print("1. Truy vấn và chuẩn bị dữ liệu MBA...")
    
    # Truy vấn InvoiceNo và Description từ Fact và Dim_Product
    query = """
    SELECT
        fs.invoiceno,
        dp.description
    FROM fact_sales fs
    JOIN dim_product dp ON fs.product_sk = dp.product_sk
    WHERE dp.description IS NOT NULL;
    """
    df_transactions = pd.read_sql_query(query, engine)
    
    # Làm sạch Description: loại bỏ khoảng trắng thừa
    df_transactions['description'] = df_transactions['description'].astype(str).str.strip()
    
    # Nhóm theo InvoiceNo và Description (sử dụng max(invoiceno) để tạo giá trị 1)
    basket = (df_transactions.groupby(['invoiceno', 'description'])['invoiceno']
              .count().unstack().reset_index().fillna(0)
              .set_index('invoiceno'))

    # Chuyển đổi số lượng thành ma trận nhị phân (có mua/không mua)
    def encode_units(x):
        return 1 if x >= 1 else 0
    
    basket_sets = basket.map(encode_units)
    
    # Loại bỏ các giao dịch đặc biệt không phải sản phẩm (ví dụ: POSTAGE)
    if 'POSTAGE' in basket_sets.columns:
        basket_sets.drop(columns=['POSTAGE'], inplace=True)
    
    print(f"   -> Đã tạo ma trận One-Hot Encoded với {len(basket_sets)} hóa đơn.")
    return basket_sets

def run_apriori(basket_sets):
    """
    2. Chạy Thuật toán Apriori và 3. Trích xuất Quy tắc.
    """
    print("2. Chạy thuật toán Apriori...")
    
    # Tham số mẫu (như đề xuất):
    MIN_SUPPORT = 0.015  # Ngưỡng Support tối thiểu: 1.5%
    MIN_CONFIDENCE = 0.4 # Ngưỡng Confidence tối thiểu: 40%
    MIN_LIFT = 1.2       # Ngưỡng Lift tối thiểu: 1.2
    
    # Tìm Frequent Itemsets
    frequent_itemsets = apriori(basket_sets, min_support=MIN_SUPPORT, use_colnames=True)
    
    print(f"   -> Tìm thấy {len(frequent_itemsets)} tập hợp sản phẩm thường xuyên.")

    # Trích xuất Association Rules
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=MIN_LIFT)
    
    # Lọc theo Confidence
    rules = rules[(rules['confidence'] >= MIN_CONFIDENCE)]
    
    print(f"   -> Trích xuất được {len(rules)} quy tắc kết hợp mạnh.")
    
    # Sắp xếp và làm sạch cột
    rules = rules.sort_values(['lift'], ascending=False).reset_index(drop=True)
    rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
    rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))

    return rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]

if __name__ == '__main__':
    try:
        basket_sets = prepare_mba_input(engine)
        association_rules_df = run_apriori(basket_sets)
        
        os.makedirs(os.path.dirname(OUTPUT_RULES_PATH), exist_ok=True)
        association_rules_df.to_csv(OUTPUT_RULES_PATH, index=False)
        
        print(f"\n✅ Market Basket Analysis hoàn tất. Quy tắc đã lưu tại: {OUTPUT_RULES_PATH}")
        
        print("\n--- TOP 5 QUY TẮC MẠNH NHẤT (Lift Cao nhất) ---")
        print(association_rules_df.head(5).to_markdown(index=False))

    except Exception as e:
        print(f"\nLỗi khi chạy MBA: {e}")