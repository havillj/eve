from features import *

chromNumbers = {'1': 'NC_035107.1', '2': 'NC_035108.1', '3': 'NC_035109.1'}

def main():
    makeIntervalTrees()
    
    text = input('Query (chr start end / "left" / "right"): ')
    while text not in 'Qq':
        parts = text.split()
        seqid = chromNumbers[parts[0]]
        if parts[2] == 'left':
            end = int(parts[1])
            start = end - FEATURE_SEARCH_DIST
        elif parts[2] == 'right':
            start = int(parts[1])
            end = start + FEATURE_SEARCH_DIST
        else:
            start = int(parts[1])
            end = int(parts[2])
        feats = searchiTrees(seqid, start, end)
        if parts[2] == 'left':
            feats.sort(key=lambda t: t[2].end, reverse=True)
        elif parts[2] == 'right':
            feats.sort(key=lambda t: t[2].start)
        features = []
        for type, id, location in feats:
            if parts[2] == 'left':
                if location.end <= end:
                    print('*{0:,} - {1:,} {2:}: {3:}'.format(location.start, location.end, type, id))
                else:
                    print('{0:,} - {1:,} {2:}: {3:}'.format(location.start, location.end, type, id))
            elif parts[2] == 'right':
                if location.start >= start:
                    print('*{0:,} - {1:,} {2:}: {3:}'.format(location.start, location.end, type, id))
                else:
                    print('{0:,} - {1:,} {2:}: {3:}'.format(location.start, location.end, type, id))
            else:
                print('{0:,} - {1:,} {2:}: {3:}'.format(location.start, location.end, type, id))
                
            if id != 'dust' and id != 'trf' and id[:3] != 'rnd':
                if 'LTR' in id:
                    c = 'gold'
                elif type == 'gene':
                    c = 'lightgray'
                else:
                    c = 'blue'
                    
                open_left = open_right = False
                f_start = location.start
                f_end = location.end
                if location.start < start:
                    f_start = start
                    open_left = True
                if location.end > end:
                    f_end = end
                    open_right = True
                features.append(GraphicFeature(start=f_start, end=f_end, strand=1, color=c, label = id, thickness = 12, fontdict = {'size': 6}, linewidth = 0, open_left=open_left, open_right=open_right))
    
        fig, ax = pyplot.subplots(1, 1, figsize = (10, 5))
        ax.tick_params(labelsize = 6)
        record = GraphicRecord(features = features, first_index=start, sequence_length = end-start+1)
        record.plot(ax = ax, figure_width=10)
        fig.savefig('chr' + str(parts[0]) + '_' + str(start) + '-' + str(end) + '.pdf')
        
        text = input('Query (chr start end / "left" / "right"): ')
main()