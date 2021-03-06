state_to_idx = {
    "盒子一":0,
    "盒子二":1,
    "盒子三":2,
}
idx_to_state = {
    0:"盒子一",
    1:"盒子二",
    2:"盒子三",
}
label_to_idx = {
    "红":0,
    "白":1,
    'unk':0,
}
idx_to_label = {
    0:"红",
    1:"白",
}
A = [[0.5,0.2,0.3],
     [0.3,0.5,0.2],
     [0.2,0.3,0.5]]
B = [[0.5,0.5],
     [0.4,0.6],
     [0.7,0.3]]

pi = [0.2,0.4,0.4]
class HMM():
    def __init__(self,A,B,init_distribution,
                     state_to_idx,idx_to_state,
                     label_to_idx,idx_to_label):
        self.A = A
        self.B = B
        self.pi = init_distribution
        self.state_to_idx = state_to_idx
        self.idx_to_state = idx_to_state
        self.label_to_idx = label_to_idx
        self.idx_to_label = idx_to_label
        self.N = len(A)
        self.M = len(B)
    def forward_alpha(self,label_seqs):
        label_seqs_idxs = [self.label_to_idx.get(label,label_to_idx['unk']) for label in label_seqs]
        T = len(label_seqs)
        last_alpha,tmp_alpha = [],[]
        start = label_seqs_idxs[0]
        last_alpha = [self.pi[i] * self.B[i][start] for i in range(self.N)]
        for t in range(1,T):
            label = label_seqs_idxs[t]
            tmp_alpha = [sum([last_alpha[j]*self.A[j][i]*self.B[i][label] for j in range(self.N)])
                          for i in range(self.N)]
            last_alpha = tmp_alpha
        return sum(tmp_alpha)
    def viterbi(self,label_seqs):
        label_seqs_idxs = [self.label_to_idx.get(label,label_to_idx['unk']) for label in label_seqs]
        T = len(label_seqs)
        last_alpha,tmp_alpha = [],[]
        start = label_seqs_idxs[0]
        last_alpha = [self.pi[i] * self.B[i][start] for i in range(self.N)]
        parent_state = [[] for j in range(T)]
        for t in range(1,T):
            label = label_seqs_idxs[t]
            tmp_alpha = [max([last_alpha[j] * self.A[j][i] * self.B[i][label] for j in range(self.N)])
                         for i in range(self.N)]
            parent_state[t] = [self.argmax([last_alpha[j] * self.A[j][i] for j in range(self.N)])
                         for i in range(self.N)]
            last_alpha = tmp_alpha
        ans = []
        parent = self.argmax(tmp_alpha)
        ans.append(parent)
        for t in range(T-1,0,-1):
            parent = parent_state[t][parent]
            ans.append(parent)
        return max(tmp_alpha),list(reversed(ans))

    def argmax(self,vector):
        max_item,max_idx = vector[0],0
        for i,item in enumerate(vector):
            if max_item < item:
                max_idx,max_item = i,item
        return max_idx
def main():
    hmm = HMM(A,B,pi,state_to_idx,idx_to_state,label_to_idx,idx_to_label)
    label_seqs = "红,白,红".split(",")
    #print("%.5f"%hmm.forward_alpha(label_seqs))
    best_path_pro,path = hmm.viterbi(label_seqs)
    print(path)
if __name__ == "__main__":
    main()