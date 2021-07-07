ADO_PS=0.4;
NPatchesRange=5;
NPatchesAzimuth=5;
density_rand=1;
weed_standard_dev=0.6;
weed_time_win=365;
merge_resample_size=100;
unwrap_grid_size=100;
unwrap_time_win=365;
masterdate='20200413';

cmd=['mt_prep_snap ' masterdate ' ' pwd '/Export ' num2str(ADO_PS) ' ' num2str(NPatchesRange) ' ' num2str(NPatchesAzimuth) ' 50 50'];
cmd

system(cmd);

stamps(1,1);


setparm('density_rand',density_rand);
setparm('weed_standard_dev',weed_standard_dev);
setparm('weed_time_win',weed_time_win);
setparm('merge_resample_size',merge_resample_size);
setparm('unwrap_grid_size',unwrap_grid_size);
setparm('unwrap_time_win',unwrap_grid_size);




stamps(2,5);











