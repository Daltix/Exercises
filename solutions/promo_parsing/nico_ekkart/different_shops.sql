SELECT COUNT(*) AS number_of_shops FROM (
	SELECT DISTINCT shop FROM promo_strings
) AS different_shop_query;
