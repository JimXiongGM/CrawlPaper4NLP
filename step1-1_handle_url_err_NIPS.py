import requests,os 
from utils import get_headers_cookies, simple_clean_text

proxies = {'http': 'socks5://127.0.0.1:1080','https': 'socks5://127.0.0.1:1080'}

# 手动处理NIPS的遗漏情况
text = '''/home/d/papers_data/NIPS/NIPS_2017/Variational Inference via chi Upper Bound Minimization.pdf@#@https://papers.nips.cc/paper/6866-variational-inference-via-chi-upper-bound-minimization.pdf
/home/d/papers_data/NIPS/NIPS_2017/Sparse Embedded k-Means Clustering.pdf@#@https://papers.nips.cc/paper/6924-sparse-embedded-k-means-clustering.pdf
/home/d/papers_data/NIPS/NIPS_2017/Influence Maximization with varepsilon-Almost Submodular Threshold Functions.pdf@#@https://papers.nips.cc/paper/6970-influence-maximization-with-varepsilon-almost-submodular-threshold-functions.pdf
/home/d/papers_data/NIPS/NIPS_2017/Approximation Algorithms for ell_0-Low Rank Approximation.pdf@#@https://papers.nips.cc/paper/7242-approximation-algorithms-for-ell_0-low-rank-approximation.pdf
/home/d/papers_data/NIPS/NIPS_2018/Doubly Robust Bayesian Inference for Non-Stationary Streaming Data with beta-Divergences.pdf@#@https://papers.nips.cc/paper/7292-doubly-robust-bayesian-inference-for-non-stationary-streaming-data-with-beta-divergences.pdf
/home/d/papers_data/NIPS/NIPS_2018/ell_1-regression with Heavy-tailed Distributions.pdf@#@https://papers.nips.cc/paper/7386-neural-nearest-neighbors-networks.pdf
/home/d/papers_data/NIPS/NIPS_2018/Solving Non-smooth Constrained Programs with Lower Complexity than mathcal{O}(1 varepsilon) A Primal-Dual Homotopy Smoothing Approach.pdf@#@https://papers.nips.cc/paper/7656-heterogeneous-bitwidth-binarization-in-convolutional-neural-networks.pdf
/home/d/papers_data/NIPS/NIPS_2018/Computing Kantorovich-Wasserstein Distances on d-dimensional histograms using (d+1)-partite graphs.pdf@#@https://papers.nips.cc/paper/7822-neural-interaction-transparency-nit-disentangling-learned-interactions-for-improved-interpretability.pdf
/home/d/papers_data/NIPS/NIPS_2018/Streaming Kernel PCA with tilde{O}( sqrt{n}) Random Features.pdf@#@https://papers.nips.cc/paper/7962-refuel-exploring-sparse-features-in-deep-reinforcement-learning-for-fast-disease-diagnosis.pdf
/home/d/papers_data/NIPS/NIPS_2018/Revisiting ( epsilon, gamma, tau)-similarity learning for domain adaptation.pdf@#@https://papers.nips.cc/paper/7970-how-to-tell-when-a-clustering-is-approximately-correct-using-convex-relaxations.pdf
/home/d/papers_data/NIPS/NIPS_2018/Distributed k-Clustering for Data with Heavy Noise.pdf@#@https://papers.nips.cc/paper/8010-beyond-log-concavity-provable-guarantees-for-sampling-multi-modal-distributions-using-simulated-tempering-langevin-monte-carlo.pdf
/home/d/papers_data/NIPS/NIPS_2018/Thwarting Adversarial Examples An L_0-Robust Sparse Fourier Transform.pdf@#@https://papers.nips.cc/paper/8212-blockwise-parallel-decoding-for-deep-autoregressive-models.pdf
/home/d/papers_data/NIPS/NIPS_2019/Direct Optimization through arg max for Discrete Variational Auto-Encoder.pdf@#@https://papers.nips.cc/paper/8851-direct-optimization-through-arg-max-for-discrete-variational-auto-encoder.pdf
/home/d/papers_data/NIPS/NIPS_2019/Unsupervised Co-Learning on G-Manifolds Across Irreducible Representations.pdf@#@https://papers.nips.cc/paper/9105-unsupervised-co-learning-on-g-manifolds-across-irreducible-representations.pdf
/home/d/papers_data/NIPS/NIPS_2019/Average Case Column Subset Selection for Entrywise ell_1-Norm Loss.pdf@#@https://papers.nips.cc/paper/9201-average-case-column-subset-selection-for-entrywise-ell_1-norm-loss.pdf
/home/d/papers_data/NIPS/NIPS_2019/Comparing distributions ell_1 geometry improves kernel two-sample testing.pdf@#@https://papers.nips.cc/paper/9398-comparing-distributions-ell_1-geometry-improves-kernel-two-sample-testing.pdf
/home/d/papers_data/NIPS/NIPS_2019/Outlier-robust estimation of a sparse linear model using ell_1-penalized Huber's M-estimator.pdf@#@https://papers.nips.cc/paper/9477-outlier-robust-estimation-of-a-sparse-linear-model-using-ell_1-penalized-hubers-m-estimator.pdf'''


folder = './papers_data'


def test():
    for line in text.strip().split('\n'):
        org = line.split('@#@')[0].split('/')[-3]
        org_year = line.split('@#@')[0].split('/')[-2]
        year = org_year[-4:]
        name = line.split('@#@')[0].split('/')[-1]
        url = line.split('@#@')[-1]
        headers, cookies = get_headers_cookies('NIPS', year)
        with requests.Session() as s:
            r = s.get(url, headers = headers, cookies = cookies, proxies = proxies)
        print(f'len: {len(r.content)}.\t{name} ')
        
        if len(r.content) < 100:
            print('ERROR')
            continue

        if not os.path.exists(f'{folder}/{org}/{org_year}'): os.makedirs(f'{folder}/{org}/{org_year}')
        file_name = f'{folder}/{org}/{org_year}/{name}'
        with open(file_name, 'wb') as f1:
            f1.write(r.content)
    return None


if __name__ == "__main__":
    test()


