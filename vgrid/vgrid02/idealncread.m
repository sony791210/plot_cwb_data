clc; clear all;clf
salt=ncread('1_temp.nc','temp');                         %�n��
nodeid=load('nodeid.txt');                             %�n��,�ƶq��n+1
nodenum= length(nodeid(:,1))-1;    % node number 
transec=load('transect1.out');
% for j=1:nodenum
% transec(j,:)=transec2(nodeid(j+1),:);
% end 
timestart=72;                                          %�n��,nc�ɪ��ɶ�
timeend  =480;                                         %�n��
Climax   =32;                                         %�n��
Climin   =10;                                         %�n��
Cspace   =1;                                         %�n��
% contourspace=10;
datestart=18 ;                                         %�n��        
nodedp=transec(:,6);                          
for i=1:nodenum-1
nodedis(i,1)=transec(i+1,5)-transec(i,5);                      %,�ƶq��n-1
end 
nodedis(:,2)=round(nodedis(:,1)/10);
% vlayer = length(transec(1,:))-7;    % vertical layer                      %,�������h��
vlayer = 29;    % vertical layer                      %,�������h��
maxdp =   ceil(max(nodedp)*1.1);   % maximun water depth in drewmap         %�n��
                                                                     %%%�ܤU���s�ɪ����|��ø�ϳ]�w ���i�H��
maxdis=  sum(nodedis(1:nodenum-1,2));
maxdrate=1;
[xi, yi] = meshgrid(1:1:maxdis, 1:1:maxdp*maxdrate);%
ts2e=timeend-timestart;
tide=ncread('1_elev.nc','elev',[nodeid(2,1),timestart],[1,ts2e]);    %�n��

%%
nodedis(1,3)=1;
count1=nodedis(1,3);
for k=2:nodenum
    count1=count1+nodedis(k-1,2);
    nodedis(k,3)=count1;
   
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for time=timestart:timeend;
for k=1:nodenum;
    s(time,k,1:vlayer)=salt(nodeid(k+1,1),1:vlayer,time);
end
end
%%
elevcount=0
%%%%%%%%%%%%%%%Data input%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for time=timestart:timeend;
    for node=1:nodenum;
        for vlay=1:vlayer;
             if s(time,node,vlay) == -9999;
              s(time,node,vlay) = NaN;
             end
         ma(vlay,node)=s(time,node,vlay);
        end
     end
 %%%%%%%%%%%%%%% vertical layer interpoly to depth matrix %%%%
%interp1(�px , salt�� , �jx , '��k')
%���B�z�px
%��X�C���I���h��
    for c1= 1:nodenum          %-- how many layers in each colunm
          rec1(1,c1)=abs(transec(c1,2));
    end                        %-- how many layers in each colunm
    
    rec3(:,1)=round(interp1(nodedis(1:nodenum,3),rec1(1,1:nodenum),[1:maxdis],'linear'));
    nodedp2(:,1)=interp1(nodedis(1:nodenum,3),nodedp(1:nodenum,1),[1:maxdis],'linear');
  %-------------interp  , �ھڼh�ƨӤ��t��J�ȭn�h�jX����m
   posi(1:vlayer,1:vlayer) = 0;
   posib(1:vlayer,1:vlayer) = 0; 
   count=0;
   for n=1:nodenum;     %�� 
      
%           posi(j,n)=round(nodedp(n,1)*(j/rec1(1,n)));
          r11=rec1(1,n)-1; r12=r11+8;
          posi(1:rec1(1,n),n)=abs(transec(n,8:r12));
         posib(1:rec1(1,n),n)=maxdrate*posi(1:rec1(1,n),n);%
            posib(1,n)=0.00001;%
          
        rec=rec1(1,n); %
       rec2=vlayer-rec1(1,n)+1;%
       xposi(1+count:rec+count,1) = nodedis(n,3)  ;%     
       yposi(1+count:rec+count,1) = posib(1:rec,n) ;%
       sb=double(ma(vlayer:-1:rec2,n));%
       zposi(1+count:rec+count,1) = sb;%
       count=rec1(1,n)+count    ;%
   end    
         zi2 = griddata(xposi,yposi, zposi, xi, yi);%
         zi = roundn(zi2(:,:),-4);%    
% %          %     %**********���Ԫ�l��     
%          for m=1:length(zi(1,:));
%          zi(1:length(zi(:,1)),m) = zi(1:length(zi(:,1)),495);
%          end
% %          %     %**********���Ԫ�l��     
%           zi=zi+0.2;
        for n=1:maxdis;%%���y�����a��
            rec=nodedp2(n,1)*maxdrate;%
            maxyi=length(yi(:,n));%
            zi(rec+1:maxyi,n)=NaN;%
        end    %
       %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%        subplot(5,4,[1:16]);
%         set(gca,'Clim',[Climin,Climax]);
       [cs,hs]=contourf(xi, yi, zi,[Climin:Cspace:Climax],'lines','--'); %view([0,270]);% shading flat;	% �e�X����
        clabel(cs,hs,60);view([0,270]);%
       set(gca,'Clim',[Climin,Climax]);
        colorbar;
%            hold on; plot(xposi, yposi, 'o','MarkerSize',3,'MarkerFaceColor','k'); hold off
          dayz=fix(time/24); hrz=mod(time,24);
          
          ds=datestart+floor((time+0)/24) ;
          if (ds >= 30); 
              month=10;
          else
              month=09;
          end  
          dsm=mod(ds,30);
          if (dsm == 0);
              dsm=1;
          end
%           string2=['KP-','Temperature (C)','-','2018 /',num2str(month),' /' ,num2str(dsm),' ',num2str(mod(time+0,24)),':00'];
          string2=['Day' ,num2str(fix(time/24)),' hr',num2str(mod(time+0,24))];
%            string2=['Day0' ' hr0'];
          title(string2,'fontsize',14);
%           xlabel(' ','fontsize',14); %��
          distance=round(nodedis(:,3)/100)*100;    %��
          disinkm=distance/1000 ;                 %��
          xlength=length(zi(1,:));
%       set(gca , 'xtick' ,[0 :xlength/5:xlength ]); %��
%           set(gca , 'xticklabel',[0:disinkm/5:disinkm] ,'fontsize',14); %��          
%            xticklabel('fontsize',14); %��
           ylabel('depth (m)','fontsize',14) 
           xlabel('  ','fontsize',14)
% %      set(gca,'ylim',[-0.8 0.8]);
% %********�e��
% % ts2e=timeend-timestart;
% elevcount=elevcount+1;
% % tide=ncread('1_elev.nc','elev',[nodeid(2,1),timestart],[1,ts2e]);    %�n��
% subplot(5,4,[17 18 19 20 ]);
% plot(tide,'linewidth',1.5);hold on;
% plot(elevcount,tide(elevcount),'linestyle','none','marker','.','MarkerSize',25,'MarkerEdgeColor','r');
% hold off
% tidenum=length(tide) ;  set(gca,'xtick' ,[0 :24:tidenum] );
% set(gca,'xticklabel' ,[ ] );
% set(gca,'yticklabel' ,[ ] );

%%%%%%%%%%%%%%%%% �e���_�y�t
%  subplot(5,4,[ 18 19 ]);
% tmod=mod(time,24);
% utmod=mod(tmod,12);
% spd=0.2;
% for i=1:24;
%     spdd(i)=spd*sin(2*pi*i/12);
% end    
% utspd=spd*sin(2*pi*utmod/12);
%  plot(spdd,'linewidth',1.5);hold on;
% plot(tmod,utspd,'linestyle','none','marker','.','MarkerSize',25,'MarkerEdgeColor','r');
% set(gca,'xlim',[1 24]);grid on ;
% hold off;
%%%%%%%%%%%%%%%%% �e���_�y�t
%**************
%           pause(0.001);
    ii=time+0;
   string=[num2str(ii,'%04.0f'),'.png'];

         saveas(gca,string);         %%�s�ɶ}��  
% %  end                             %%time end
     %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
end