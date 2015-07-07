# hungs the server
select dt, regn, sum(itogo *  mult) from bulk_f102_p1 f left join f102_check_codes g
on convert(f.code, unsigned) = g.code 
